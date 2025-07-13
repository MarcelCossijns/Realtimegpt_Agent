async def execute_tool(hass, tool_call):
    domain = tool_call.function.name.split('.')[0]
    service = tool_call.function.name.split('.')[1]
    data = tool_call.function.arguments
    await hass.services.async_call(domain, service, data)