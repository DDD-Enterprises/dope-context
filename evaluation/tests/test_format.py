import unittest

from langchain_core.messages import AIMessage, HumanMessage

from evaluation.utils.format import calculate_total_tokens


class CalculateTotalTokensTests(unittest.TestCase):
    def test_missing_usage_does_not_abort_accounting(self):
        total = calculate_total_tokens(
            {"messages": [HumanMessage(content="user"), AIMessage(content="assistant")]}
        )

        self.assertEqual(
            total,
            {
                "input_tokens": 0,
                "output_tokens": 0,
                "total_tokens": 0,
                "max_single_turn_tokens": 0,
            },
        )

    def test_missing_usage_falls_back_to_reported_provider_counts(self):
        result = calculate_total_tokens(
            {
                "messages": [
                    AIMessage(
                        content="assistant",
                        response_metadata={"usage": {"input_tokens": 4, "output_tokens": 5}},
                    ),
                    AIMessage(
                        content="assistant",
                        usage_metadata={"input_tokens": 2, "output_tokens": 3, "total_tokens": 5},
                        response_metadata={"usage": {"input_tokens": 80, "output_tokens": 20}},
                    ),
                ]
            }
        )

        self.assertEqual(
            result,
            {
                "input_tokens": 6,
                "output_tokens": 8,
                "total_tokens": 14,
                "max_single_turn_tokens": 9,
            },
        )
