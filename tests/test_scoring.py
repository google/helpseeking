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

import json
import os
import sys

import pytest

# Add the project root to sys.path to allow importing from scripts
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from scripts import scoring


def _load_complete_rubric_data():
  test_dir = os.path.dirname(__file__)
  with open(os.path.join(test_dir, 'sample_scored_rubric.json')) as f:
    scored_rubric = json.load(f)
  with open(os.path.join(test_dir, 'sample_rubric.json')) as f:
    rubric = json.load(f)
  return scored_rubric, rubric


def _load_minimal_rubric_data():
  test_dir = os.path.dirname(__file__)
  with open(os.path.join(test_dir, 'sample_scored_rubric.json')) as f:
    scored_rubric = json.load(f)
  with open(os.path.join(test_dir, 'sample_rubric_minimal_criteria.json')) as f:
    rubric = json.load(f)
  return scored_rubric, rubric


def test_scoring():
  scored_rubric, rubric = _load_complete_rubric_data()
  score = scoring.calculate_score(scored_rubric, rubric)
  assert score == 0.9


def test_calculate_score_positive_factual():
  scored_rubric, rubric = _load_complete_rubric_data()
  score = scoring.calculate_score_positive_factual(scored_rubric, rubric)
  assert score == pytest.approx(19 / 24)


def test_calculate_score_negative_factual():
  scored_rubric, rubric = _load_complete_rubric_data()
  score = scoring.calculate_score_negative_factual(scored_rubric, rubric)
  assert score == 0.0


def test_calculate_score_positive_delivery():
  scored_rubric, rubric = _load_complete_rubric_data()
  score = scoring.calculate_score_positive_delivery(scored_rubric, rubric)
  assert score == 1.0


def test_calculate_score_negative_delivery():
  scored_rubric, rubric = _load_complete_rubric_data()
  score = scoring.calculate_score_negative_delivery(scored_rubric, rubric)
  assert score == 0.0


def test_calculate_score_negative_factual_absent():
  scored_rubric, rubric = _load_minimal_rubric_data()
  score = scoring.calculate_score_negative_factual(scored_rubric, rubric)

  # When a rubric is missing negative factual criteria, the scoring
  # function returns None.
  assert score is None


def test_calculate_score_positive_factual_absent():
  scored_rubric, rubric = _load_minimal_rubric_data()
  score = scoring.calculate_score_positive_factual(scored_rubric, rubric)

  # All rubrics are guaranteed to have positive factual criteria.
  assert score == pytest.approx(19 / 24)


def test_calculate_score_positive_delivery_absent():
  scored_rubric, rubric = _load_minimal_rubric_data()
  score = scoring.calculate_score_positive_delivery(scored_rubric, rubric)

  # When a rubric is missing positive delivery criteria, the scoring
  # function returns None.
  assert score is None


def test_calculate_score_negative_delivery_absent():
  scored_rubric, rubric = _load_minimal_rubric_data()
  score = scoring.calculate_score_negative_delivery(scored_rubric, rubric)

  # All rubrics are guaranteed to have negative delivery criteria.
  assert score == 0.0
