import httpx
from mcp.server.fastmcp import FastMCP, Context
from lunarcalendar import Converter, Solar, Lunar

# Initialize the MCP server
mcp = FastMCP("LunarBirthday", dependencies=["lunarcalendar"])

@mcp.resource("lunar_birthday://{year}/{month}/{day}")
def get_lunar_birthday(year: int, month: int, day: int) -> str:
    """
    Get the lunar birthday based on the solar birth date.
    """
    try:
        solar_date = Solar(year, month, day)
        lunar_date = Converter.Solar2Lunar(solar_date)
        return f"{lunar_date.year}-{lunar_date.month}-{lunar_date.day}"
    except ValueError:
        return f"Error: Invalid date '{year}-{month}-{day}'"

@mcp.tool()
def get_lunar_birthday_tool(ctx: Context, year: int, month: int, day: int) -> str:
    """
    Get detailed lunar birthday information based on solar birth date.
    """
    try:
        solar_date = Solar(year, month, day)
        lunar_date = Converter.Solar2Lunar(solar_date)
        
        # 中文月份映射
        lunar_month_names = ['正', '二', '三', '四', '五', '六', '七', '八', '九', '十', '冬', '腊']
        # 中文日期映射
        lunar_day_prefix = ['初', '十', '廿', '卅']
        lunar_day_suffix = ['一', '二', '三', '四', '五', '六', '七', '八', '九', '十']
        
        month_name = lunar_month_names[lunar_date.month - 1]
        
        if lunar_date.day == 10:
            day_name = '初十'
        elif lunar_date.day == 20:
            day_name = '二十'
        elif lunar_date.day == 30:
            day_name = '三十'
        else:
            prefix_index = (lunar_date.day - 1) // 10
            suffix_index = (lunar_date.day - 1) % 10
            day_name = lunar_day_prefix[prefix_index] + lunar_day_suffix[suffix_index]
        
        lunar_str = f"阴历生日: {lunar_date.year}年{month_name}月{day_name}日"
        ctx.info(f"Successfully retrieved lunar birthday for {year}-{month}-{day}")
        return lunar_str
    except ValueError as e:
        ctx.error(f"Failed to fetch lunar birthday: {str(e)}")
        return f"Error: {str(e)}"

@mcp.prompt()
def lunar_birthday_prompt() -> str:
    """Prompt template for asking about lunar birthday"""
    return "请根据我的阳历生日获取阴历生日，格式为 '年/月/日'。"

if __name__ == "__main__":
    mcp.run()
