from collections.abc import Generator
from typing import Any

import requests

from dify_plugin import Tool
from dify_plugin.entities.tool import ToolInvokeMessage

SERP_API_URL = "https://serpapi.com/search"


class GoogleSearchTool(Tool):
	def _parse_response(self, response: dict) -> dict:
		result = {}
		if "knowledge_graph" in response:
			result["title"] = response["knowledge_graph"].get("title", "")
			result["description"] = response["knowledge_graph"].get("description", "")
		if "organic_results" in response:
			result["organic_results"] = [
				{
					"title": item.get("title", ""),
					"link": item.get("link", ""),
					"snippet": item.get("snippet", ""),
				}
				for item in response["organic_results"]
			]
		print(result)
		return result

	def _invoke(self, tool_parameters: dict[str, Any]) -> Generator[ToolInvokeMessage]:
		params = {
			"api_key": self.runtime.credentials["serpapi_api_key"],
			"q": tool_parameters["query"],
			"engine": "google",
			"google_domain": "google.com",
			"gl": "us",
			"hl": "en",
		}
		print("q:", tool_parameters["query"])
		response = requests.get(url=SERP_API_URL, params=params, timeout=5)
		response.raise_for_status()
		valuable_res = self._parse_response(response.json())

		yield self.create_json_message(valuable_res)