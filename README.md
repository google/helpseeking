# Help-seeking and help-giving: Datasets for understanding privacy, safety, and security questions and model response quality.

This repository contains data and associated code for understanding real-world user questions that focus on privacy, safety, and security, and the quality of LLM responses to those questions.

## Help-seeking dataset

This dataset consists of over 4 million questions posted on Reddit from 2021--2025 that involved a user seeking help with privacy, safety, or security. The dataset is available in `datasets/help_seeking.jsonl.zip`.

### Annotations

Each line in the dataset is a JSON object consisting of the following fields:

- `permalink`: The original link of the Reddit post. We do not include any text from the post, so this must be retrieved.
- `account_tools`: Boolean indicating the post includes topics related to account recovery (including cryptocurrency wallets), account security configurations (e.g., 2FA, SMS authentication), forgotten passwords, password managers, or inaccessible accounts or devices.
- `privacy_tools`: Boolean indicating the post includes topics related to popular privacy tools (e.g., Tor, VPNs), configuring privacy settings (e.g., cookies, E2EE), data controls (e.g., permissions, settings), or general privacy topics (e.g., preventing tracking).
- `safety_tools`: Boolean indicating the post includes topics related platform-provided safety tools such as blocking, reporting, takedown, and other moderation tools.
- `security_tools`: Boolean indicating the post includes topics related to popular security tools (e.g., anti-virus, hardware cryptocurrency wallets), security practices (e.g., encryption, access control, logging, firewalls), or general security topics (e.g., jailbreaking, network security).
- `compromise`: Boolean indicating the post includes topics related to users who suspect or describe behavior that suggest their account or device may have been compromised. Topics include account hacking, suspicious sign-ins or OTPs, malware, or suspicious files.
- `platform_actions`: Boolean indicating the post includes topics related to users experiencing friction with platform policies or safety barriers. Topics include being banned, suspended, or falsely reported; access being blocked to websites or services; or transactions being incorrectly flagged as fraud.
- `scams`: Boolean indicating the post includes topics related to users experiencing scams or fraud. Topics include fake job postings, sextortion, spam, unauthorized transactions, stolen funds (including cryptocurrencies), or suspicious webpages or links.
- `harassment`: Boolean indicating the post includes topics related to users experiencing harassment or sexual abuse. Topics include toxic comments, stalking, doxxing, grooming, interpersonal abuse, or image-based sexual abuse (e.g., cyberflashing, non-consensual explicit imagery).
- `data_concerns`: Boolean indicating the post includes topics related to users concerned about their data being exposed, misused, or inappropriately collected. Topics include oversharing, breaches, retention, collection, and consent.

More details on the dataset construction can be found in [our paper](https://arxiv.org/abs/2601.11398).

## Help-giving benchmark

This dataset contains HelpBench, a benchmark of 450 questions across user needs related to privacy, safety, and security. The benchmark is available in `datasets/helpbench.jsonl`. Topics in the benchmark match those of the help-seeking dataset (e.g., `account_tools`, `privacy_tools`, `safety_tools`, `security_tools`, `compromise`, `platform_actions`, `scams`, `harassment`, `data_concerns`).

### Annotations

Each question in HelpBench is a JSON object consisting of the following fields:

- `id`: A unique numeric identifier for the question.
- `question_text`: The text of the question that should be posed to a model.
- `primary_topic`: Manually-determined label of the primary topic of the question.
- `annotations`: A dictionary of boolean values indicating whether any topics appear in the question, as well as other properties of questions, such as:
    - `mentions_practice`: A boolean indicating whether or not the question mentions an existing practice (i.e., something someone has done to try to address their concern).
    - `is_sensemaking`: A boolean indicating whether the question is trying to better understand the situation (e.g., "Is this safe?").
    - `is_guidance`: A boolean indicating whether the question is seeking how to act in a given situation (e.g., "How do I change this permission?").
    - `is_therapeutic`: A boolean indicating whether the question is seeking reassurance, validation, or social support (e.g., "Is feeling this way normal?").
- `rubric`: The expert-developed scoring rubric for the question. Each item in this list contains the following fields:
    - `id`: A unique identifier for the criterion.
    - `criterion`: The statement of the criterion.
    - `at_beginning`: A boolean indicating whether or not the criterion should be met at the beginning of the response. This is used to guide the autorater in evaluating the criterion "The most important information is at the beginning", if present in the rubric.
    - `points`: The number of points associated with the criterion. This can be -5, -3, -2, -1, 1, 2, 3, or 5.


More details on the construction of the benchmark and how experts were involved in creating rubrics can be found in [our paper]().

### Running an autorater

The repository contains a template for the autorater prompt in `scripts/autorater.py`. To run the autorater, this template needs to be filled with (1) the question being evaluated (`question`), (2) the response to that question (`response`), and (3) the rubric associated with the question (`rubric`).

### Scoring autorater responses

Responses earn points for both meeting criteria with positive associated points (capturing the good things they did) and for avoiding meeting criteria with negative associated points (capturing the bad things they avoided doing). We capture this way of scoring in the `calculate_score` function in `scripts/scoring.py`.


To test scoring, we have provided a unit test in `tests/test_scoring.py`. This test loads `tests/sample_scored_rubric.json`, `tests/sample_rubric_minimal_criteria.json`, and `tests/sample_rubric.json` and verifies that the scores match the expected values.


To run the tests, ensure you have `pytest` and `absl-py` installed, and execute the following command from the project root:


```bash
$ pytest
```

### Improving autorater performance

To evaluate other autorater models or autorater prompts, use `datasets/helpbench_expert_rater.json` as ground truth. Each entry contains the following fields:

- `id`: A unique identifier for the rubric associated with the entry, mapping to `datasets/helpbench.jsonl`.
- `question_text`: The text of the question posed to a model.
- `model_response`: The response from a randomly selected model.
- `expert_scored_rubric`: The scored rubric for the question with an experts' decisions for whether each criterion was met or not.
- `expert_score`: The overall score for the model response based on the experts' decisions.


## Disclaimer

This is not an officially supported Google product. This project is not
eligible for the [Google Open Source Software Vulnerability Rewards
Program](https://bughunters.google.com/open-source-security).


This project is intended for demonstration purposes only. It is not
intended for use in a production environment.
