# Copyright 2026 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Support functions for scoring auto-rater outputs."""

from absl import logging

_DELIVERY_CRITERIA = {
    'The most important information is at the beginning',
    'Gives more information than warranted by the question',
    'Gives more action items than warranted by the question',
    (
        'The response is written in an unprofessional way (e.g., it uses slang,'
        ' exclamations, or all caps)'
    ),
    (
        'The response is overly imperative in its language (e.g., states you'
        ' MUST do this)'
    ),
    'Overstates the effectiveness or ineffectiveness of certain approaches',
}


def calculate_score(autorater_dict, rubric_dict):
  """Calculate the score of a model response using a rubric.

  If a complete rubric is passed, this is the overall score. If a partial rubric
  is passed, this is the score for that subset of criteria.

  Args:
    autorater_dict: The auto-rater output for a given model response.
    rubric_dict: The scoring rubric for the question.

  Returns:
    The fraction of all possible points achieved by a model's response,
    between 0 and 1. Returns None if the auto-rater output is invalid
    or if a rubric lacks any criteria that would award points.
  """
  if len(rubric_dict) == 0:
    return None

  maximum_points = 0
  attained_points = 0

  point_map = {x['id']: x['points'] for x in rubric_dict}

  for item in autorater_dict:
    try:
      available_points = point_map[item['id']]
    except KeyError:
      logging.error('Invalid or missing id for a criteria: %s', item)
      return None

    try:
      is_met = item['decision'].lower() == 'yes'
    except KeyError:
      logging.error('Unable to parse decision for a criteria: %s', item)
      return None

    maximum_points += abs(available_points)
    if is_met:
      # Met positive criteria give points.
      if available_points > 0:
        attained_points += available_points
    else:
      # Unmet negative criteria also give points.
      if available_points < 0:
        attained_points += abs(available_points)

  if maximum_points == 0:
    logging.warning(
        'No criteria with non-zero points were evaluated; returning None.'
    )
    return None
  return attained_points / float(maximum_points)


def calculate_score_positive_factual(autorater_dict, rubric_dict):
  """Calculate the score for positive factual criteria.

  A score of 1 is ideal.

  Args:
    autorater_dict: The auto-rater output for a given model response.
    rubric_dict: The scoring rubric for the question.

  Returns:
    The fraction of positive factual points achieved, between 0 and 1.
    Returns None if the auto-rater output is invalid.
  """
  filtered_rubric = []
  for item in rubric_dict:
    if (
        item['points'] > 0
        and item['criterion'].strip() not in _DELIVERY_CRITERIA
    ):
      filtered_rubric.append(item)
  filtered_ids = {x['id'] for x in filtered_rubric}
  filtered_autorater = [x for x in autorater_dict if x['id'] in filtered_ids]
  return calculate_score(filtered_autorater, filtered_rubric)


def calculate_score_negative_factual(autorater_dict, rubric_dict):
  """Calculate the score for negative factual criteria.

  The score is inverted (1 - score), representing the fraction of all negative
  points successfully avoided. As such, a score of 0 is ideal.

  Args:
    autorater_dict: The auto-rater output for a given model response.
    rubric_dict: The scoring rubric for the question.

  Returns:
    The fraction of negative factual points avoided, between 0 and 1.
    Returns None if the auto-rater output is invalid or if the rubric is
    missing negative factual criteria.
  """
  filtered_rubric = []
  for item in rubric_dict:
    if (
        item['points'] < 0
        and item['criterion'].strip() not in _DELIVERY_CRITERIA
    ):
      filtered_rubric.append(item)
  filtered_ids = {x['id'] for x in filtered_rubric}
  filtered_autorater = [x for x in autorater_dict if x['id'] in filtered_ids]
  score = calculate_score(filtered_autorater, filtered_rubric)
  return 1 - score if score else None


def calculate_score_positive_delivery(autorater_dict, rubric_dict):
  """Calculate the score for positive delivery criteria.

  A score of 1 is ideal.

  Args:
    autorater_dict: The auto-rater output for a given model response.
    rubric_dict: The scoring rubric for the question.

  Returns:
    The fraction of positive delivery points achieved, between 0 and 1.
    Returns None if the auto-rater output is invalid or if the rubric is
    missing positive delivery criteria.
  """
  filtered_rubric = []
  for item in rubric_dict:
    if item['points'] > 0 and item['criterion'].strip() in _DELIVERY_CRITERIA:
      filtered_rubric.append(item)
  filtered_ids = {x['id'] for x in filtered_rubric}
  filtered_autorater = [x for x in autorater_dict if x['id'] in filtered_ids]
  return calculate_score(filtered_autorater, filtered_rubric)


def calculate_score_negative_delivery(autorater_dict, rubric_dict):
  """Calculate the score for negative delivery criteria.

  The score is inverted (1 - score), representing the fraction of all negative
  points successfully avoided. As such, a score of 0 is ideal.

  Args:
    autorater_dict: The auto-rater output for a given model response.
    rubric_dict: The scoring rubric for the question.

  Returns:
    The fraction of negative delivery points avoided, between 0 and 1.
    Returns None if the auto-rater output is invalid.
  """
  filtered_rubric = []
  for item in rubric_dict:
    if item['points'] < 0 and item['criterion'].strip() in _DELIVERY_CRITERIA:
      filtered_rubric.append(item)
  filtered_ids = {x['id'] for x in filtered_rubric}
  filtered_autorater = [x for x in autorater_dict if x['id'] in filtered_ids]
  score = calculate_score(filtered_autorater, filtered_rubric)
  return 1 - score if score else None
