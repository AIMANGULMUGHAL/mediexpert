"""
MEDIEXPERT
Inference Engine

Rule-based forward-chaining-style inference engine.

Features:
- Evaluates predefined medical rules
- Uses selected symptoms as facts
- Calculates transparent rule-match scores
- Filters weak matches
- Groups multiple rules belonging to the same condition
- Keeps the strongest rule for each condition
- Returns transparent reasoning
- Limits dashboard results to the strongest matches

NOTE:
This is an educational rule-based system and does not provide
medical diagnosis or medical advice.
"""

from knowledge_base import KNOWLEDGE_BASE, SYMPTOM_LABELS


# ============================================================
# CONFIGURATION
# ============================================================

# Minimum score required for a rule to be considered relevant.
MIN_MATCH_SCORE = 60

# Maximum number of conditions displayed on the dashboard.
MAX_RESULTS = 5

# Maximum number of reasoning rules displayed for each condition.
MAX_REASONING_RULES_PER_CONDITION = 3


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def calculate_rule_match(selected_symptoms, rule):
    """
    Calculate how strongly a predefined rule matches
    the selected symptoms.

    Required symptoms:
        80% of total score

    Optional symptoms:
        20% of total score

    A rule is considered fired only when it reaches the
    minimum score threshold.
    """

    selected = set(selected_symptoms)

    required = list(rule.get("required", []))
    optional = list(rule.get("optional", []))

    # --------------------------------------------------------
    # Find matching required symptoms
    # --------------------------------------------------------

    matched_required = [
        symptom
        for symptom in required
        if symptom in selected
    ]

    # --------------------------------------------------------
    # Find matching optional symptoms
    # --------------------------------------------------------

    matched_optional = [
        symptom
        for symptom in optional
        if symptom in selected
    ]

    # --------------------------------------------------------
    # Find missing symptoms
    # --------------------------------------------------------

    missing_required = [
        symptom
        for symptom in required
        if symptom not in selected
    ]

    missing_optional = [
        symptom
        for symptom in optional
        if symptom not in selected
    ]

    # --------------------------------------------------------
    # Calculate required score
    # --------------------------------------------------------

    if required:
        required_score = (
            len(matched_required) / len(required)
        )
    else:
        required_score = 0

    # --------------------------------------------------------
    # Calculate optional score
    # --------------------------------------------------------

    if optional:
        optional_score = (
            len(matched_optional) / len(optional)
        )
    else:
        optional_score = 0

    # --------------------------------------------------------
    # Weighted score
    # --------------------------------------------------------

    score = (
        required_score * 80
        +
        optional_score * 20
    )

    score = round(min(score, 100))

    # --------------------------------------------------------
    # Rule firing logic
    #
    # IMPORTANT:
    # A rule no longer fires simply because 50% of its
    # required symptoms are present.
    #
    # It must reach the minimum score threshold.
    # --------------------------------------------------------

    rule_fired = score >= MIN_MATCH_SCORE

    return {
        "score": score,

        "matched_required": matched_required,

        "matched_optional": matched_optional,

        "missing_required": missing_required,

        "missing_optional": missing_optional,

        "rule_fired": rule_fired,

        # Correct evidence count.
        "matched_count": (
            len(matched_required)
            +
            len(matched_optional)
        ),

        "required_count": len(required),

        "optional_count": len(optional),

        "total_rule_symptoms": (
            len(required)
            +
            len(optional)
        ),
    }


# ============================================================
# REASONING CREATOR
# ============================================================

def create_reasoning(rule, evaluation):
    """
    Convert a rule evaluation into transparent reasoning
    information for the frontend.
    """

    evidence = []

    # --------------------------------------------------------
    # Required evidence
    # --------------------------------------------------------

    for symptom in evaluation["matched_required"]:

        evidence.append({
            "symptom": symptom,

            "label": SYMPTOM_LABELS.get(
                symptom,
                symptom
            ),

            "type": "required",

            "matched": True,
        })

    # --------------------------------------------------------
    # Optional/supporting evidence
    # --------------------------------------------------------

    for symptom in evaluation["matched_optional"]:

        evidence.append({
            "symptom": symptom,

            "label": SYMPTOM_LABELS.get(
                symptom,
                symptom
            ),

            "type": "supporting",

            "matched": True,
        })

    # --------------------------------------------------------
    # Missing evidence
    # --------------------------------------------------------

    missing = []

    for symptom in evaluation["missing_required"]:

        missing.append({
            "symptom": symptom,

            "label": SYMPTOM_LABELS.get(
                symptom,
                symptom
            ),

            "type": "required",
        })

    for symptom in evaluation["missing_optional"]:

        missing.append({
            "symptom": symptom,

            "label": SYMPTOM_LABELS.get(
                symptom,
                symptom
            ),

            "type": "supporting",
        })

    # --------------------------------------------------------
    # Rule statistics
    # --------------------------------------------------------

    matched_count = evaluation["matched_count"]

    total_rule_symptoms = evaluation[
        "total_rule_symptoms"
    ]

    # Example:
    #
    # 3 matching facts / 3 rule facts
    #
    evidence_summary = (
        f"{matched_count} / "
        f"{total_rule_symptoms} "
        f"matching facts"
    )

    # --------------------------------------------------------
    # Explanation
    # --------------------------------------------------------

    explanation = (
        f"The rule for {rule['condition']} "
        f"matched {evaluation['score']}% "
        f"of its defined symptom pattern."
    )

    return {
        "rule_id": rule["id"],

        "condition": rule["condition"],

        "required_labels": [
            SYMPTOM_LABELS.get(
                symptom,
                symptom
            )
            for symptom in rule.get(
                "required",
                []
            )
        ],

        "optional_labels": [
            SYMPTOM_LABELS.get(
                symptom,
                symptom
            )
            for symptom in rule.get(
                "optional",
                []
            )
        ],

        "evidence": evidence,

        "missing": missing,

        "score": evaluation["score"],

        "fired": evaluation["rule_fired"],

        "matched_count": matched_count,

        "required_count": evaluation[
            "required_count"
        ],

        "optional_count": evaluation[
            "optional_count"
        ],

        "total_rule_symptoms": total_rule_symptoms,

        "evidence_summary": evidence_summary,

        "explanation": explanation,

        "guidance": rule.get(
            "guidance",
            "Consider discussing persistent or concerning symptoms with a qualified healthcare professional."
        ),
    }


# ============================================================
# CONDITION GROUPING
# ============================================================

def group_rules_by_condition(reasoning_items):
    """
    Merge multiple rules belonging to the same condition.

    Example:

        R017 -> COVID-like Respiratory Infection Pattern
        R018 -> COVID-like Respiratory Infection Pattern

    become ONE condition result.

    The strongest rule determines the primary score.
    """

    condition_map = {}

    for reasoning in reasoning_items:

        condition = reasoning["condition"]

        if condition not in condition_map:

            condition_map[condition] = {
                "condition": condition,

                "score": reasoning["score"],

                "rules": [],

                "guidance": reasoning["guidance"],

                "best_rule": reasoning,

            }

        condition_map[condition]["rules"].append(
            reasoning
        )

        # ----------------------------------------------------
        # Keep strongest rule
        # ----------------------------------------------------

        if (
            reasoning["score"]
            >
            condition_map[condition]["score"]
        ):

            condition_map[condition]["score"] = (
                reasoning["score"]
            )

            condition_map[condition]["guidance"] = (
                reasoning["guidance"]
            )

            condition_map[condition]["best_rule"] = (
                reasoning
            )

    return condition_map


# ============================================================
# BUILD RESULT
# ============================================================

def build_condition_result(condition_data):
    """
    Create the clean result object returned to the frontend.
    """

    best_rule = condition_data["best_rule"]

    # Sort rules belonging to this condition.
    rules = sorted(
        condition_data["rules"],
        key=lambda item: item["score"],
        reverse=True
    )

    # Keep only the strongest reasoning rules.
    rules = rules[
        :MAX_REASONING_RULES_PER_CONDITION
    ]

    return {
        "condition": condition_data["condition"],

        "score": condition_data["score"],

        "rank": 0,

        "rule_id": best_rule["rule_id"],

        "matched_count": best_rule[
            "matched_count"
        ],

        "total_rule_symptoms": best_rule[
            "total_rule_symptoms"
        ],

        "evidence": best_rule[
            "evidence"
        ],

        "missing": best_rule[
            "missing"
        ],

        "required_labels": best_rule[
            "required_labels"
        ],

        "optional_labels": best_rule[
            "optional_labels"
        ],

        "guidance": condition_data[
            "guidance"
        ],

        "rules": rules,
    }


# ============================================================
# MAIN INFERENCE FUNCTION
# ============================================================

def analyze_symptoms(selected_symptoms):
    """
    Main MEDIEXPERT inference function.

    Input:
        selected_symptoms:
            list of symptom identifiers

    Example:

        [
            "fever",
            "cough",
            "fatigue",
            "body_aches"
        ]

    Output:
        {
            "success": True,
            "results": [...],
            "reasoning": [...],
            "selected_symptoms": [...]
        }
    """

    # ========================================================
    # STEP 1
    # Clean input
    # ========================================================

    if not selected_symptoms:

        return {
            "success": True,

            "results": [],

            "reasoning": [],

            "selected_symptoms": [],

            "message": (
                "Please select at least one symptom "
                "before starting the analysis."
            ),
        }

    # --------------------------------------------------------
    # Remove duplicates while preserving order.
    # --------------------------------------------------------

    selected_symptoms = list(
        dict.fromkeys(selected_symptoms)
    )

    # ========================================================
    # STEP 2
    # Convert symptoms into FACTS
    # ========================================================

    facts = set(selected_symptoms)

    # ========================================================
    # STEP 3
    # Evaluate every predefined rule
    # ========================================================

    evaluated_rules = []

    for rule in KNOWLEDGE_BASE:

        evaluation = calculate_rule_match(
            facts,
            rule
        )

        # ----------------------------------------------------
        # Only accept strong rules.
        # ----------------------------------------------------

        if evaluation["rule_fired"]:

            reasoning = create_reasoning(
                rule,
                evaluation
            )

            evaluated_rules.append(
                reasoning
            )

    # ========================================================
    # STEP 4
    # Sort rules by strongest match
    # ========================================================

    evaluated_rules.sort(
        key=lambda item: item["score"],
        reverse=True
    )

    # ========================================================
    # STEP 5
    # Merge duplicate conditions
    # ========================================================

    condition_map = group_rules_by_condition(
        evaluated_rules
    )

    # ========================================================
    # STEP 6
    # Build clean condition results
    # ========================================================

    results = []

    for condition_data in condition_map.values():

        result = build_condition_result(
            condition_data
        )

        results.append(result)

    # ========================================================
    # STEP 7
    # Rank conditions
    # ========================================================

    results.sort(
        key=lambda item: item["score"],
        reverse=True
    )

    # ========================================================
    # STEP 8
    # Limit dashboard results
    # ========================================================

    results = results[:MAX_RESULTS]

    # ========================================================
    # STEP 9
    # Add rank
    # ========================================================

    for index, result in enumerate(
        results,
        start=1
    ):

        result["rank"] = index

    # ========================================================
    # STEP 10
    # Keep reasoning only for displayed conditions
    # ========================================================

    displayed_conditions = {
        result["condition"]
        for result in results
    }

    reasoning = [
        item
        for item in evaluated_rules
        if item["condition"]
        in displayed_conditions
    ]

    # ========================================================
    # STEP 11
    # No strong match
    # ========================================================

    if not results:

        return {
            "success": True,

            "results": [],

            "reasoning": [],

            "selected_symptoms": selected_symptoms,

            "message": (
                "No strong predefined rule matched "
                "the selected symptoms. This does not "
                "rule out any medical condition."
            ),

            "threshold": MIN_MATCH_SCORE,
        }

    # ========================================================
    # STEP 12
    # Return final expert-system output
    # ========================================================

    return {
        "success": True,

        "results": results,

        "reasoning": reasoning,

        "selected_symptoms": selected_symptoms,

        "message": (
            "Analysis completed using the predefined "
            "rule-based knowledge base."
        ),

        "threshold": MIN_MATCH_SCORE,
    }


# ============================================================
# OPTIONAL DEBUG FUNCTION
# ============================================================

def get_engine_settings():
    """
    Return current inference-engine settings.

    Useful for displaying system information
    during development/demo.
    """

    return {
        "minimum_match_score": MIN_MATCH_SCORE,

        "maximum_results": MAX_RESULTS,

        "maximum_reasoning_rules_per_condition": (
            MAX_REASONING_RULES_PER_CONDITION
        ),

        "rule_based": True,

        "random_generation": False,
    }