"""
Unit tests for Calculator MCP Server
Tests all calculator operations and error handling

Run with: pytest tests/test_calculator.py -v
"""
import json
import pytest
import sys
import os

# Add parent directory to path to import calc_server
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from calc_server import _add as add, _subtract as subtract, _multiply as multiply, _divide as divide


class TestAddition:
    """Test add operation"""

    def test_add_positive_numbers(self):
        """Test adding two positive numbers"""
        result = json.loads(add(5, 3))
        assert result["operation"] == "add"
        assert result["a"] == 5
        assert result["b"] == 3
        assert result["result"] == 8

    def test_add_negative_numbers(self):
        """Test adding two negative numbers"""
        result = json.loads(add(-5, -3))
        assert result["result"] == -8

    def test_add_mixed_signs(self):
        """Test adding positive and negative numbers"""
        result = json.loads(add(10, -3))
        assert result["result"] == 7

    def test_add_zero(self):
        """Test adding zero"""
        result = json.loads(add(5, 0))
        assert result["result"] == 5

    def test_add_decimals(self):
        """Test adding decimal numbers"""
        result = json.loads(add(2.5, 3.7))
        assert abs(result["result"] - 6.2) < 0.0001

    def test_add_large_numbers(self):
        """Test adding large numbers"""
        result = json.loads(add(1000000, 2000000))
        assert result["result"] == 3000000


class TestSubtraction:
    """Test subtract operation"""

    def test_subtract_positive_numbers(self):
        """Test subtracting two positive numbers"""
        result = json.loads(subtract(10, 3))
        assert result["operation"] == "subtract"
        assert result["a"] == 10
        assert result["b"] == 3
        assert result["result"] == 7

    def test_subtract_negative_result(self):
        """Test subtraction resulting in negative"""
        result = json.loads(subtract(3, 10))
        assert result["result"] == -7

    def test_subtract_negative_numbers(self):
        """Test subtracting negative numbers"""
        result = json.loads(subtract(-5, -3))
        assert result["result"] == -2

    def test_subtract_zero(self):
        """Test subtracting zero"""
        result = json.loads(subtract(5, 0))
        assert result["result"] == 5

    def test_subtract_from_zero(self):
        """Test subtracting from zero"""
        result = json.loads(subtract(0, 5))
        assert result["result"] == -5

    def test_subtract_decimals(self):
        """Test subtracting decimal numbers"""
        result = json.loads(subtract(10.5, 3.2))
        assert abs(result["result"] - 7.3) < 0.0001


class TestMultiplication:
    """Test multiply operation"""

    def test_multiply_positive_numbers(self):
        """Test multiplying two positive numbers"""
        result = json.loads(multiply(4, 5))
        assert result["operation"] == "multiply"
        assert result["a"] == 4
        assert result["b"] == 5
        assert result["result"] == 20

    def test_multiply_by_zero(self):
        """Test multiplying by zero"""
        result = json.loads(multiply(5, 0))
        assert result["result"] == 0

    def test_multiply_negative_numbers(self):
        """Test multiplying two negative numbers"""
        result = json.loads(multiply(-3, -4))
        assert result["result"] == 12

    def test_multiply_mixed_signs(self):
        """Test multiplying positive and negative"""
        result = json.loads(multiply(-3, 4))
        assert result["result"] == -12

    def test_multiply_decimals(self):
        """Test multiplying decimal numbers"""
        result = json.loads(multiply(2.5, 4))
        assert result["result"] == 10.0

    def test_multiply_large_numbers(self):
        """Test multiplying large numbers"""
        result = json.loads(multiply(1000, 1000))
        assert result["result"] == 1000000


class TestDivision:
    """Test divide operation"""

    def test_divide_positive_numbers(self):
        """Test dividing two positive numbers"""
        result = json.loads(divide(10, 2))
        assert result["operation"] == "divide"
        assert result["a"] == 10
        assert result["b"] == 2
        assert result["result"] == 5

    def test_divide_by_zero(self):
        """Test division by zero returns error"""
        result = json.loads(divide(10, 0))
        assert "error" in result
        assert "divide by zero" in result["error"].lower()

    def test_divide_resulting_in_decimal(self):
        """Test division resulting in decimal"""
        result = json.loads(divide(7, 2))
        assert result["result"] == 3.5

    def test_divide_negative_numbers(self):
        """Test dividing negative numbers"""
        result = json.loads(divide(-10, 2))
        assert result["result"] == -5

    def test_divide_by_negative(self):
        """Test dividing by negative number"""
        result = json.loads(divide(10, -2))
        assert result["result"] == -5

    def test_divide_decimals(self):
        """Test dividing decimal numbers"""
        result = json.loads(divide(7.5, 2.5))
        assert result["result"] == 3.0

    def test_divide_zero_by_number(self):
        """Test dividing zero by a number"""
        result = json.loads(divide(0, 5))
        assert result["result"] == 0


class TestJSONFormat:
    """Test JSON response format consistency"""

    def test_success_response_has_required_fields(self):
        """Test successful response has all required fields"""
        result = json.loads(add(1, 2))
        assert "operation" in result
        assert "a" in result
        assert "b" in result
        assert "result" in result

    def test_all_operations_return_valid_json(self):
        """Test all operations return valid JSON"""
        operations = [
            add(1, 2),
            subtract(5, 3),
            multiply(4, 2),
            divide(10, 2)
        ]
        for op_result in operations:
            # Should not raise JSONDecodeError
            parsed = json.loads(op_result)
            assert isinstance(parsed, dict)

    def test_error_response_format(self):
        """Test error response has error field"""
        result = json.loads(divide(1, 0))
        assert "error" in result
        assert isinstance(result["error"], str)
        assert len(result["error"]) > 0


class TestEdgeCases:
    """Test edge cases and boundary conditions"""

    def test_very_small_decimals(self):
        """Test operations with very small decimal numbers"""
        result = json.loads(add(0.0001, 0.0002))
        assert abs(result["result"] - 0.0003) < 0.00001

    def test_operations_with_integers_as_floats(self):
        """Test that integer inputs work (type: float accepts int)"""
        result = json.loads(add(5, 3))
        assert result["result"] == 8

    def test_result_type_consistency(self):
        """Test that results are numeric types"""
        operations = [
            json.loads(add(1, 2)),
            json.loads(subtract(5, 3)),
            json.loads(multiply(4, 2)),
            json.loads(divide(10, 2))
        ]
        for op in operations:
            if "result" in op:
                assert isinstance(op["result"], (int, float))


if __name__ == "__main__":
    # Run tests with pytest
    pytest.main([__file__, "-v"])
