"""Site manifest: mirrors docs.deeptutor.info/zh-cn/ sidebar structure."""

SECTIONS = [
    ("總覽", [
        ("index", "文件主頁"),
        ("contributing", "參與貢獻"),
    ]),
    ("快速上手", [
        ("get-started/index", "概覽"),
        ("get-started/pypi", "1 · PyPI 安裝"),
        ("get-started/from-source", "2 · 源碼安裝"),
        ("get-started/docker", "3 · Docker"),
        ("get-started/cli-only", "4 · 純 CLI 安裝"),
        ("get-started/multi-user", "多使用者部署"),
        ("get-started/providers", "模型與搜尋提供商"),
        ("get-started/troubleshooting", "故障排查"),
    ]),
    ("探索 DeepTutor", [
        ("explore/chat-workspace", "主頁"),
        ("explore/partners", "夥伴"),
        ("explore/mastery-path", "精通之路"),
        ("explore/reading", "沉浸式閱讀"),
        ("explore/book", "書籍"),
        ("explore/subagents", "我的智慧代理"),
        ("explore/co-writer", "智慧寫作"),
        ("explore/knowledge", "知識空間"),
        ("explore/space", "學習空間"),
        ("explore/memory", "記憶"),
        ("explore/settings", "設定"),
    ]),
    ("DeepTutor 生態", [
        ("ecosystem/index", "生態概覽"),
        ("ecosystem/skills", "Skill 擴充"),
        ("ecosystem/mcp", "MCP 擴充"),
        ("ecosystem/cli-apps", "CLI-App 擴充"),
        ("ecosystem/rag-integration", "RAG 整合"),
        ("ecosystem/eduhub", "EduHub"),
    ]),
    ("夥伴與管道", [
        ("partners/index", "概覽"),
        ("partners/channels", "管道矩陣"),
        ("partners/weixin", "個人微信"),
        ("partners/wecom", "企業微信"),
        ("partners/qq", "QQ / NapCat"),
        ("partners/telegram", "Telegram"),
        ("partners/discord", "Discord"),
        ("partners/slack", "Slack"),
        ("partners/feishu", "飛書 / Lark"),
        ("partners/dingtalk", "釘釘"),
        ("partners/matrix", "Matrix"),
        ("partners/zulip", "Zulip"),
        ("partners/mattermost", "Mattermost"),
        ("partners/whatsapp", "WhatsApp"),
        ("partners/email", "郵件"),
        ("partners/mochat", "Mochat"),
        ("partners/msteams", "Microsoft Teams"),
    ]),
    ("DeepTutor CLI", [
        ("cli/index", "概覽"),
        ("cli/commands", "命令參考"),
        ("cli/chat-repl", "互動式 REPL"),
        ("cli/agent-handoff", "代理交接"),
        ("cli/python-sdk", "Python SDK"),
        ("cli/server-api", "伺服器端 API"),
    ]),
]

# slug -> source md (defaults to "<slug>.md")
SOURCE_OVERRIDES = {
    "index": "index.md",
    "contributing": "contributing.md",
    "cli/index": "cli.md",
    "ecosystem/index": "ecosystem.md",
    "get-started/index": "get-started.md",
    "partners/index": "partners.md",
}


def flat_pages():
    """[(slug, label, section)] in sidebar order (also the pager order)."""
    out = []
    for section, items in SECTIONS:
        for slug, label in items:
            out.append((slug, label, section))
    return out


def pages_dict():
    return {slug: (label, section) for slug, label, section in flat_pages()}


def source_path(slug):
    name = SOURCE_OVERRIDES.get(slug, slug + ".md")
    return name
