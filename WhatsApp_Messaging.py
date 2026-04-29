import os
import json
import httpx
from mcp.server.fastmcp import FastMCP

"""
Sample credentials.json (place this file in the same directory):

[
  {
    "whatsapp_business_profile": "WABA1",
    "phone_number_id": "123456789012345",
    "api_access_token": "EAAJZCXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
  },
  {
    "whatsapp_business_profile": "WABA2",
    "phone_number_id": "987654321098765",
    "api_access_token": "EAAJZBYYYYYYYYYYYYYYYYYYYYYYYYYYYY"
  }
]
"""

# Initialize the FastMCP server
mcp = FastMCP(
    "WhatsApp Messaging Server",
    host="0.0.0.0",
    port=7030
)

def _get_credentials_by_whatsapp_profile(whatsapp_business_profile: str) -> tuple[str, str]:
    """
    Reads credentials.json and returns the (phone_number_id, api_access_token) 
    for the matching whatsapp_business_profile.
    """
    try:
        with open("credentials.json", "r") as f:
            credentials = json.load(f)
    except FileNotFoundError:
        raise Exception("Error: credentials.json file not found in the current directory.")
    except json.JSONDecodeError:
        raise Exception("Error: credentials.json contains invalid JSON.")

    for cred in credentials:
        if cred.get("whatsapp_business_profile") == whatsapp_business_profile:
            phone_number_id = cred.get("phone_number_id")
            api_access_token = cred.get("api_access_token")
            
            if not phone_number_id or not api_access_token:
                raise ValueError(f"Missing phone_number_id or api_access_token for app '{whatsapp_business_profile}'")
                
            return phone_number_id, api_access_token
            
    raise ValueError(f"App name '{whatsapp_business_profile}' was not found in credentials.json.")

def list_whatsapp_profiles() -> list[str]:
    """Returns a list of all available app names from credentials.json."""
    try:
        with open("credentials.json", "r") as f:
            credentials = json.load(f)
        return [cred.get("whatsapp_business_profile") for cred in credentials if cred.get("whatsapp_business_profile")]
    except Exception:
        return []

async def _send(payload: dict, whatsapp_business_profile: str) -> dict:
    """
    Internal helper function to send the payload to the WhatsApp Cloud API.
    Dynamically fetches credentials based on the provided whatsapp_business_profile.
    """
    phone_number_id, api_access_token = _get_credentials_by_whatsapp_profile(whatsapp_business_profile)
    print(phone_number_id, api_access_token)
    url = f"https://graph.facebook.com/v24.0/{phone_number_id}/messages"
    
    headers = {
        "Authorization": f"Bearer {api_access_token}",
        "Content-Type": "application/json"
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(url, headers=headers, json=payload)
        
        if response.status_code >= 400:
            raise Exception(f"WhatsApp API Error {response.status_code}: {response.text}")
            
        return response.json()

@mcp.tool()
def list_whatsapp_profiles() -> list[str]:
    """
    List all available WhatsApp app profiles configured in credentials.json.
    Call this first if you are unsure which whatsapp_business_profile to use.

    Returns:
        A list of available app names.
    """
    profiles = list_whatsapp_profiles()
    if not profiles:
        return ["No profiles found. Please check your credentials.json file."]
    return profiles

@mcp.tool()
async def send_whatsapp_text(
    whatsapp_business_profile: str,
    to_phone_number: str,
    message: str
) -> str:
    """
    Send a standard text message via WhatsApp using a specific app profile.
    If you don't know which whatsapp_business_profile to use, call list_whatsapp_apps first.

    Args:
        whatsapp_business_profile: The name of the app profile to use (e.g., 'Telenetix' or 'whp').
        to_phone_number: The recipient's phone number with country code (e.g., '15551234567').
        message: The text message to send.
    """
    payload = {
        "messaging_product": "whatsapp",
        "recipient_type": "individual",
        "to": to_phone_number,
        "type": "text",
        "text": {
            "preview_url": False,
            "body": message
        }
    }
    
    result = await _send(payload, whatsapp_business_profile)
    message_id = result.get("messages", [{}])[0].get("id", "Unknown ID")
    return f"Message sent successfully using '{whatsapp_business_profile}'! Message ID: {message_id}"

@mcp.tool()
async def send_whatsapp_template(
    whatsapp_business_profile: str,
    to_phone_number: str, 
    template_name: str, 
    language_code: str = "en", 
    components: list | None = None
) -> str:
    """
    Send a templated WhatsApp message using a specific app profile.
    If you don't know which whatsapp_business_profile to use, call list_whatsapp_apps first.

    Args:
        whatsapp_business_profile: The name of the app profile to use (e.g., 'Telenetix' or 'whp').
        to_phone_number: The recipient's phone number with country code.
        template_name: The name of the approved WhatsApp template.
        language_code: The language code of the template (default: en).
        components: Optional list of dicts for template variables (headers, body params, buttons, etc.).
    """
    payload = {
        "messaging_product": "whatsapp",
        "to": to_phone_number,
        "type": "template",
        "template": {
            "name": template_name,
            "language": {
                "code": language_code
            }
        }
    }
    
    if components:
        payload["template"]["components"] = components

    result = await _send(payload, whatsapp_business_profile)
    message_id = result.get("messages", [{}])[0].get("id", "Unknown ID")
    return f"Template '{template_name}' sent successfully using '{whatsapp_business_profile}'! Message ID: {message_id}"

if __name__ == "__main__":
    mcp.run(transport="streamable-http")
