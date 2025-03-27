import pytest
from unittest.mock import AsyncMock, patch
from agent import agent, check_streaming_availability

# Unit tests for the check_streaming_availability tool
@pytest.mark.asyncio
async def test_check_streaming_availability_valid_title():
    """Test the tool with a valid title that returns streaming information"""
    mock_response = "Available on Netflix, Amazon Prime"
    with patch('agent_tools.query_streaming_availability', new=AsyncMock(return_value=mock_response)):
        result = await check_streaming_availability(None, "Inception")
        assert result == mock_response

@pytest.mark.asyncio
async def test_check_streaming_availability_title_not_found():
    """Test the tool with a title that's not available on any platform"""
    mock_response = "No streaming options found for this title"
    with patch('agent_tools.query_streaming_availability', new=AsyncMock(return_value=mock_response)):
        result = await check_streaming_availability(None, "Non-existent Movie")
        assert result == mock_response

@pytest.mark.asyncio
async def test_check_streaming_availability_empty_title():
    """Test the tool with an empty title input"""
    with patch('agent_tools.query_streaming_availability', new=AsyncMock()) as mock_query:
        result = await check_streaming_availability(None, "")
        assert "Please provide a valid title" in result
        mock_query.assert_not_awaited()

# Integration tests for agent interaction
@pytest.mark.asyncio
async def test_agent_responds_with_streaming_info():
    """Test that the agent properly uses the tool and returns streaming info"""
    test_cases = [
        ("Where can I watch The Matrix?", "Netflix"),
        ("Is Interstellar available for streaming?", "Amazon Prime"),
        ("How can I stream Breaking Bad?", "Netflix")
    ]

    for query, service in test_cases:
        with patch('agent_tools.query_streaming_availability', new=AsyncMock(return_value=f"Available on {service}")):
            response = await agent.run(query)
            assert service in response, f"Expected {service} in response for query: {query}"

@pytest.mark.asyncio
async def test_agent_handles_unavailable_title():
    """Test agent response when a title isn't available"""
    mock_response = "No streaming options found"
    with patch('agent_tools.query_streaming_availability', new=AsyncMock(return_value=mock_response)):
        response = await agent.run("Where can I watch Unknown Movie 2025?")
        assert "not available" in response.lower() or "no streaming" in response.lower()

@pytest.mark.asyncio
async def test_agent_prompts_for_valid_title():
    """Test agent response when given empty input"""
    response = await agent.run("")
    assert "provide a movie or TV show title" in response.lower()

# Edge case test for special characters
@pytest.mark.asyncio
async def test_special_characters_title():
    """Test titles with special characters"""
    mock_response = "Available on Disney+"
    with patch('agent_tools.query_streaming_availability', new=AsyncMock(return_value=mock_response)):
        result = await check_streaming_availability(None, "Loki: Season 2")
        assert "Disney+" in result