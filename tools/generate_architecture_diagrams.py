#!/usr/bin/env python3
"""Generate five 16:9 production architecture diagrams as editable SVG files."""

from __future__ import annotations

from html import escape
from pathlib import Path


WIDTH = 1920
HEIGHT = 1080
OUT_DIR = Path(__file__).resolve().parents[1] / "architecture-diagrams"
FONT = "'WenQuanYi Micro Hei','Microsoft YaHei','PingFang SC',sans-serif"

NAVY = "#102A43"
INK = "#243B53"
MUTED = "#627D98"
LINE = "#BCCCDC"
BG = "#F5F8FC"
WHITE = "#FFFFFF"
BLUE = "#1473E6"
CYAN = "#0E9FAD"
GREEN = "#14866D"
AMBER = "#D97706"
RED = "#D64545"
PURPLE = "#7656C9"


class SVG:
    def __init__(self, title: str, subtitle: str, number: str):
        self.parts: list[str] = [
            f'<svg xmlns="http://www.w3.org/2000/svg" width="{WIDTH}" height="{HEIGHT}" '
            f'viewBox="0 0 {WIDTH} {HEIGHT}" role="img" aria-label="{escape(title)}">',
            "<defs>",
            '<filter id="shadow" x="-20%" y="-20%" width="140%" height="150%">'
            '<feDropShadow dx="0" dy="5" stdDeviation="7" flood-color="#102A43" flood-opacity=".12"/>'
            "</filter>",
            '<filter id="soft" x="-20%" y="-20%" width="140%" height="150%">'
            '<feDropShadow dx="0" dy="2" stdDeviation="3" flood-color="#102A43" flood-opacity=".09"/>'
            "</filter>",
            '<marker id="arrow-blue" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="8" markerHeight="8" orient="auto">'
            '<path d="M 0 0 L 10 5 L 0 10 z" fill="#1473E6"/></marker>',
            '<marker id="arrow-green" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="8" markerHeight="8" orient="auto">'
            '<path d="M 0 0 L 10 5 L 0 10 z" fill="#14866D"/></marker>',
            '<marker id="arrow-amber" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="8" markerHeight="8" orient="auto">'
            '<path d="M 0 0 L 10 5 L 0 10 z" fill="#D97706"/></marker>',
            "</defs>",
            f'<rect width="{WIDTH}" height="{HEIGHT}" fill="{BG}"/>',
            '<rect x="0" y="0" width="1920" height="116" fill="#FFFFFF"/>',
            '<rect x="0" y="114" width="1920" height="2" fill="#D9E2EC"/>',
            f'<text x="64" y="50" font-family="{FONT}" font-size="30" font-weight="700" fill="{NAVY}">{escape(title)}</text>',
            f'<text x="64" y="84" font-family="{FONT}" font-size="16" fill="{MUTED}">{escape(subtitle)}</text>',
            '<rect x="1600" y="31" width="256" height="48" rx="24" fill="#E7F0FC"/>',
            f'<text x="1728" y="61" text-anchor="middle" font-family="{FONT}" font-size="16" font-weight="700" fill="{BLUE}">'
            f'{escape(number)}  ·  生产环境</text>',
        ]

    def add(self, value: str) -> None:
        self.parts.append(value)

    def rect(
        self,
        x: float,
        y: float,
        w: float,
        h: float,
        fill: str = WHITE,
        stroke: str = LINE,
        rx: float = 14,
        sw: float = 1.5,
        dash: str | None = None,
        shadow: bool = False,
    ) -> None:
        dash_attr = f' stroke-dasharray="{dash}"' if dash else ""
        filter_attr = ' filter="url(#shadow)"' if shadow else ""
        self.add(
            f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{fill}" '
            f'stroke="{stroke}" stroke-width="{sw}"{dash_attr}{filter_attr}/>'
        )

    def text(
        self,
        x: float,
        y: float,
        text: str,
        size: int = 18,
        color: str = INK,
        weight: int = 400,
        anchor: str = "start",
    ) -> None:
        self.add(
            f'<text x="{x}" y="{y}" text-anchor="{anchor}" font-family="{FONT}" '
            f'font-size="{size}" font-weight="{weight}" fill="{color}">{escape(text)}</text>'
        )

    def multiline(
        self,
        x: float,
        y: float,
        lines: list[str],
        size: int = 16,
        color: str = INK,
        weight: int = 400,
        anchor: str = "start",
        leading: float = 1.35,
    ) -> None:
        spans = []
        for i, line in enumerate(lines):
            dy = 0 if i == 0 else size * leading
            spans.append(f'<tspan x="{x}" dy="{dy}">{escape(line)}</tspan>')
        self.add(
            f'<text x="{x}" y="{y}" text-anchor="{anchor}" font-family="{FONT}" '
            f'font-size="{size}" font-weight="{weight}" fill="{color}">{"".join(spans)}</text>'
        )

    def line(
        self,
        x1: float,
        y1: float,
        x2: float,
        y2: float,
        color: str = BLUE,
        sw: float = 2.5,
        arrow: str | None = "blue",
        dash: str | None = None,
    ) -> None:
        marker = f' marker-end="url(#arrow-{arrow})"' if arrow else ""
        dash_attr = f' stroke-dasharray="{dash}"' if dash else ""
        self.add(
            f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{color}" '
            f'stroke-width="{sw}" stroke-linecap="round"{marker}{dash_attr}/>'
        )

    def polyline(
        self,
        points: list[tuple[float, float]],
        color: str = BLUE,
        sw: float = 2.5,
        arrow: str | None = "blue",
        dash: str | None = None,
    ) -> None:
        point_str = " ".join(f"{x},{y}" for x, y in points)
        marker = f' marker-end="url(#arrow-{arrow})"' if arrow else ""
        dash_attr = f' stroke-dasharray="{dash}"' if dash else ""
        self.add(
            f'<polyline points="{point_str}" fill="none" stroke="{color}" stroke-width="{sw}" '
            f'stroke-linecap="round" stroke-linejoin="round"{marker}{dash_attr}/>'
        )

    def circle(self, x: float, y: float, r: float, fill: str, stroke: str = "none", sw: float = 0) -> None:
        self.add(f'<circle cx="{x}" cy="{y}" r="{r}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>')

    def pill(self, x: float, y: float, w: float, text: str, fill: str, color: str) -> None:
        self.rect(x, y, w, 30, fill=fill, stroke=fill, rx=15, sw=0)
        self.text(x + w / 2, y + 21, text, 14, color, 700, "middle")

    def card(
        self,
        x: float,
        y: float,
        w: float,
        h: float,
        title: str,
        body: list[str],
        accent: str = BLUE,
        body_size: int = 15,
        fill: str = WHITE,
    ) -> None:
        self.rect(x, y, w, h, fill=fill, stroke="#D9E2EC", rx=13, sw=1.2, shadow=True)
        self.add(f'<rect x="{x}" y="{y}" width="7" height="{h}" rx="3.5" fill="{accent}"/>')
        self.text(x + 23, y + 30, title, 18, NAVY, 700)
        if body:
            self.multiline(x + 23, y + 56, body, body_size, MUTED, 400, leading=1.28)

    def footer(self, text: str) -> None:
        self.text(64, 1044, text, 14, MUTED)
        self.text(1856, 1044, "1920 × 1080  |  16:9", 14, MUTED, 400, "end")

    def finish(self) -> str:
        return "\n".join(self.parts + ["</svg>", ""])


def diagram_1() -> SVG:
    s = SVG(
        "① 服务器集群节点与网络分区",
        "阿里云深圳地域 · 8 节点 Kubernetes 生产集群 · 双网段",
        "01 / 05",
    )

    # External entry points
    s.card(48, 176, 190, 112, "互联网用户", ["Web / APP / 渠道"], BLUE, 15)
    s.card(48, 682, 190, 142, "本地 FAST 平台", ["研发管理 / CI/CD", "连接云上 K8s 部署"], PURPLE, 15)

    # Cloud and VPC boundaries
    s.rect(270, 144, 1602, 842, fill="#F9FBFE", stroke="#8FB6E6", rx=24, sw=2)
    s.pill(300, 165, 214, "阿里云 · 深圳地域", "#E7F0FC", BLUE)
    s.rect(298, 302, 1546, 650, fill="#EFF6FD", stroke="#A7C7EB", rx=20, sw=1.8)
    s.text(326, 334, "生产 VPC（10.78.0.0/16，网段范围按现网路由表确认）", 17, NAVY, 700)

    # Purchased edge services
    edge_x = [320, 600, 880, 1160]
    edge_titles = ["域名管理 / DNS", "DDoS 攻击防护", "Web 应用防火墙 WAF", "阿里云负载均衡 SLB"]
    edge_colors = [PURPLE, RED, AMBER, BLUE]
    for x, title, color in zip(edge_x, edge_titles, edge_colors):
        s.card(x, 205, 224, 72, title, [], color)
    for x in [544, 824, 1104]:
        s.line(x + 8, 241, x + 48, 241)
    s.line(238, 232, 314, 232)

    # Cluster ingress
    s.card(1440, 205, 372, 72, "K8s Ingress / 统一网关", ["流量分发至微服务副本"], CYAN, 14)
    s.line(1384, 241, 1434, 241)
    s.line(1626, 277, 1626, 352)

    # Two network zones
    zone_specs = [
        (326, "业务节点区 A · 10.78.65.0/24", ["10.78.65.11", "10.78.65.12", "10.78.65.13", "10.78.65.14"], BLUE),
        (1082, "业务节点区 B · 10.78.68.0/24", ["10.78.68.11", "10.78.68.12", "10.78.68.13", "10.78.68.14"], CYAN),
    ]
    for zx, label, ips, color in zone_specs:
        s.rect(zx, 362, 732, 548, fill=WHITE, stroke=color, rx=18, sw=1.8)
        s.add(f'<rect x="{zx}" y="362" width="732" height="50" rx="18" fill="{color}"/>')
        s.add(f'<rect x="{zx}" y="394" width="732" height="18" fill="{color}"/>')
        s.text(zx + 24, 394, label, 18, WHITE, 700)
        for idx, ip in enumerate(ips):
            col, row = idx % 2, idx // 2
            nx = zx + 28 + col * 348
            ny = 438 + row * 177
            s.rect(nx, ny, 324, 145, fill="#F8FAFD", stroke="#C7D6E6", rx=14, sw=1.2)
            s.circle(nx + 34, ny + 37, 16, color)
            s.text(nx + 34, ny + 43, "K8s", 10, WHITE, 700, "middle")
            s.text(nx + 62, ny + 35, f"节点 {idx + 1 if zx == 326 else idx + 5}", 17, NAVY, 700)
            s.text(nx + 62, ny + 61, ip, 16, color, 700)
            s.multiline(nx + 22, ny + 94, ["Pod / Service / 容器运行时", "节点角色与工作负载由集群调度"], 14, MUTED)
        s.pill(zx + 220, 858, 292, "同一 K8s 集群 · 跨网段调度", "#EAF7F5", GREEN)

    # Internal cluster connection and FAST deployment path
    s.line(1058, 636, 1080, 636, color=CYAN, arrow="green", dash="7 6")
    s.polyline([(238, 752), (270, 752), (270, 928), (760, 928), (760, 885)], color=PURPLE, arrow=None, dash="9 7")
    s.circle(760, 885, 5, PURPLE)
    s.text(285, 924, "专线 / VPN / 受控网络连接（具体方式按现网）", 14, PURPLE, 700)

    s.rect(1478, 320, 334, 32, fill="#FFF7E6", stroke="#F3C677", rx=16, sw=1)
    s.text(1645, 342, "SLB 后端覆盖两网段节点", 14, AMBER, 700, "middle")

    s.footer("注：8 个 IP 为已知生产节点；控制面角色、VPC CIDR 与 FAST 连接方式需以阿里云现网配置为准。")
    return s


def diagram_2() -> SVG:
    s = SVG(
        "② 微服务模块分布",
        "依据《普惠系统应用架构》整理 · Kubernetes 以 Deployment / Pod 副本方式动态调度",
        "02 / 05",
    )

    # Top request and delivery paths
    s.card(56, 145, 248, 86, "渠道 / APP / 管理端", ["业务请求入口"], BLUE, 14)
    s.card(348, 145, 284, 86, "统一网关", ["Spring Cloud Gateway"], CYAN, 14)
    s.line(304, 188, 342, 188)
    s.card(1332, 145, 240, 86, "Git / Maven", ["源码与制品"], PURPLE, 14)
    s.card(1614, 145, 250, 86, "本地 FAST", ["CI/CD → 云上 K8s"], PURPLE, 14)
    s.line(1572, 188, 1608, 188, color=PURPLE, arrow=None)

    # Cluster
    s.rect(48, 263, 1816, 717, fill="#F9FBFE", stroke="#8FB6E6", rx=22, sw=2)
    s.pill(78, 280, 320, "Kubernetes 生产集群 · 8 节点", "#E7F0FC", BLUE)
    s.text(1830, 301, "10.78.65.11~14  ·  10.78.68.11~14", 14, MUTED, 700, "end")

    # Business service bands
    s.text(76, 346, "接入与终端服务", 18, NAVY, 700)
    service_cards = [
        (76, 366, 548, 110, "渠道接入服务", ["渠道接入 / 数据 / 业务处理 / 权限管理"], BLUE),
        (646, 366, 548, 110, "APP 服务", ["注册登录 / 实名认证 / 借贷申请 / 提现还款", "信息查询 / 展业管理"], BLUE),
        (1216, 366, 620, 110, "后台管理服务", ["用户角色 / 权限 / 产品 / 业务处理", "风控视图 / 运营视图"], BLUE),
    ]
    for card in service_cards:
        s.card(*card)

    s.text(76, 518, "核心业务域服务", 18, NAVY, 700)
    core_cards = [
        ("审批服务", ["流程定义 / 流转", "自动 / 人工审批"], CYAN),
        ("客户信息管理", ["客户 / 画像 / 多版本", "安全 / SSO / 查询"], CYAN),
        ("核算服务", ["借据 / 计划 / 逾期", "利息 / 计提 / 流水"], GREEN),
        ("资金管理", ["资金 / 规则配置", "额度管理"], GREEN),
        ("支付管理", ["路由 / 放款 / 扣款", "渠道接入"], AMBER),
        ("对账管理", ["交易对账", "差异处理"], AMBER),
        ("贷后催收", ["入催 / 分派 / 坐席", "诉讼 / 案件 / AI"], RED),
        ("风控 & 额度", ["名单 / 征信 / 审批", "授信 / 额度 / 结果"], RED),
    ]
    card_w = 425
    for i, (title, body, color) in enumerate(core_cards):
        x = 76 + (i % 4) * 444
        y = 538 + (i // 4) * 124
        s.card(x, y, card_w, 104, title, body, color, 14)

    # Platform components
    s.text(76, 802, "技术中台与数据支撑", 18, NAVY, 700)
    platform_groups = [
        ("治理发现", ["Nacos · Sentinel · SkyWalking"], PURPLE),
        ("调用事务", ["Feign · Ribbon · Bus · Seata"], PURPLE),
        ("任务消息", ["xxl-job · RabbitMQ"], CYAN),
        ("缓存检索", ["Redis · ElasticSearch"], GREEN),
        ("数据存储", ["MySQL · MongoDB · FastDFS · OSS"], AMBER),
    ]
    pw = 336
    for i, (title, body, color) in enumerate(platform_groups):
        s.card(76 + i * 351, 822, pw, 92, title, body, color, 14)

    # Scheduling note and links
    s.line(490, 231, 490, 360)
    s.polyline([(1738, 231), (1738, 252), (1806, 252), (1806, 277)], color=PURPLE, arrow="blue", dash="7 6")
    s.rect(1070, 927, 766, 37, fill="#EAF7F5", stroke="#A8DCD3", rx=18, sw=1)
    s.text(1453, 952, "副本由 K8s 跨 8 节点动态调度；图中不做固定 IP 绑定", 14, GREEN, 700, "middle")

    s.footer("微服务清单来源：普惠系统应用架构.pdf；“对账管理”的细分功能未在原图中展开。")
    return s


def diagram_3() -> SVG:
    s = SVG(
        "③ 安全防护组件与等保控制",
        "互联网边界 → 云上安全服务 → K8s 平台 → 应用与数据，全链路分层防护",
        "03 / 05",
    )

    # Main horizontal flow
    flow = [
        (62, 196, 250, "公网入口", ["域名 / DNS", "仅开放必要端口"], PURPLE),
        (344, 196, 250, "DDoS 防护", ["流量清洗", "攻击检测与阻断"], RED),
        (626, 196, 250, "WAF", ["OWASP 攻击防护", "Bot / 访问规则"], AMBER),
        (908, 196, 250, "SLB", ["HTTPS / TLS", "健康检查"], BLUE),
        (1190, 196, 304, "K8s Ingress / Gateway", ["入口鉴权 / 限流", "统一路由"], CYAN),
        (1526, 196, 330, "微服务与数据访问", ["服务身份 / 最小权限", "敏感数据保护"], GREEN),
    ]
    for card in flow:
        s.card(card[0], card[1], card[2], 118, card[3], card[4], card[5], 15)
    for x in [312, 594, 876, 1158, 1494]:
        s.line(x + 4, 255, x + 26, 255)

    # Boundary labels
    s.pill(76, 340, 330, "已采购阿里云安全 / 网络服务", "#EAF7F5", GREEN)
    s.pill(440, 340, 310, "K8s 与应用侧控制", "#E7F0FC", BLUE)
    s.pill(784, 340, 310, "等保加固与审计项", "#FFF3D6", AMBER)

    # Three control columns
    s.rect(62, 392, 552, 538, fill=WHITE, stroke="#A8DCD3", rx=20, sw=1.8)
    s.text(90, 431, "边界安全", 22, GREEN, 700)
    boundary = [
        ("域名管理 / DNS", "解析入口统一管理，变更留痕", GREEN),
        ("DDoS 攻击防护", "清洗公网攻击流量，配置告警", RED),
        ("Web 应用防火墙 WAF", "规则防护、黑白名单、访问日志", AMBER),
        ("安全组 / NACL", "VPC 边界防火墙，仅放通必要方向", BLUE),
        ("SLB 健康检查", "隔离异常后端，隐藏节点真实地址", BLUE),
    ]
    for i, (title, body, color) in enumerate(boundary):
        s.card(88, 454 + i * 88, 500, 72, title, [body], color, 13)

    s.rect(638, 392, 590, 538, fill=WHITE, stroke="#A7C7EB", rx=20, sw=1.8)
    s.text(666, 431, "平台与应用安全", 22, BLUE, 700)
    platform = [
        ("身份与权限", "FAST / K8s RBAC；管理员最小权限"),
        ("工作负载隔离", "Namespace、NetworkPolicy、Pod 安全策略"),
        ("密钥与证书", "K8s Secret；TLS 证书集中轮换"),
        ("应用防护", "Gateway 鉴权；Sentinel 限流与熔断"),
        ("镜像与发布", "FAST 流水线准入、镜像扫描、版本可追溯"),
    ]
    for i, (title, body) in enumerate(platform):
        s.card(664, 454 + i * 88, 538, 72, title, [body], BLUE if i < 3 else PURPLE, 13)

    s.rect(1252, 392, 604, 538, fill=WHITE, stroke="#F3C677", rx=20, sw=1.8)
    s.text(1280, 431, "加密、审计与等保要求", 22, AMBER, 700)
    compliance = [
        ("传输加密", "公网 HTTPS/TLS；服务间加密按敏感级别启用"),
        ("存储加密", "OSS SSE / 数据库加密能力（按现网启用）"),
        ("日志审计", "WAF、SLB、K8s、应用、数据库日志统一留存"),
        ("备份恢复", "数据库备份、OSS 版本化与恢复演练"),
        ("持续合规", "漏洞修复、基线核查、账号复核、等保测评"),
    ]
    for i, (title, body) in enumerate(compliance):
        s.card(1278, 454 + i * 88, 552, 72, title, [body], AMBER, 13)

    s.footer("图例：绿色=已知已采购能力；蓝/紫=平台控制；橙色=需结合等保级别与现网配置核验的加固项。")
    return s


def diagram_4() -> SVG:
    s = SVG(
        "④ 存储部署：OSS 与数据库",
        "业务数据、缓存、消息、检索和文件对象分流；未提供的数据库地址与 HA 形态明确待确认",
        "04 / 05",
    )

    # Application source
    s.rect(52, 170, 452, 728, fill="#F9FBFE", stroke="#8FB6E6", rx=22, sw=2)
    s.pill(78, 192, 316, "K8s 生产集群 · 8 节点", "#E7F0FC", BLUE)
    app_cards = [
        ("业务微服务", ["审批 / 客户 / 核算 / 资金", "支付 / 对账 / 催收 / 风控"], BLUE),
        ("统一网关", ["Spring Cloud Gateway"], CYAN),
        ("后台任务", ["xxl-job / 批处理"], PURPLE),
        ("可观测性", ["SkyWalking / 应用日志"], GREEN),
    ]
    for i, card in enumerate(app_cards):
        s.card(80, 252 + i * 132, 396, 108, *card, body_size=14)

    # Data service area
    s.rect(568, 170, 778, 728, fill="#FFFFFF", stroke="#A8DCD3", rx=22, sw=2)
    s.pill(594, 192, 360, "VPC 数据服务区 / 集群内有状态服务", "#EAF7F5", GREEN)
    s.text(1316, 213, "实际地址与部署边界待现网确认", 13, AMBER, 700, "end")

    storage_cards = [
        (596, 252, 352, 132, "MySQL", ["交易与关系型业务数据", "主从 / 集群形态待确认"], GREEN),
        (966, 252, 352, 132, "MongoDB", ["文档型业务数据", "副本集形态待确认"], GREEN),
        (596, 408, 352, 132, "Redis", ["缓存 / 会话 / 热点数据", "哨兵或集群形态待确认"], RED),
        (966, 408, 352, 132, "RabbitMQ", ["异步消息 / 业务解耦", "镜像队列或集群待确认"], AMBER),
        (596, 564, 352, 132, "ElasticSearch", ["全文检索 / 索引数据", "节点与副本数待确认"], PURPLE),
        (966, 564, 352, 132, "FastDFS", ["原架构中的分布式文件存储", "与 OSS 的边界需统一"], BLUE),
    ]
    for card in storage_cards:
        s.card(*card)
    s.rect(596, 724, 722, 138, fill="#F8FAFD", stroke="#C7D6E6", rx=15, sw=1.2)
    s.text(620, 756, "持久化与保护", 18, NAVY, 700)
    s.multiline(620, 787, ["数据库 / 中间件持久卷（PV）仅在实际部署于 K8s 时适用", "备份、保留周期、恢复点与跨区容灾目标需按生产要求配置"], 14, MUTED)

    # OSS managed service
    s.rect(1410, 170, 458, 728, fill="#FFF9EF", stroke="#F3C677", rx=22, sw=2)
    s.pill(1438, 192, 268, "阿里云托管对象存储", "#FFF3D6", AMBER)
    s.card(1438, 252, 402, 166, "OSS 存储", ["合同 / 影像 / 附件 / 导出文件", "应用通过 Endpoint + SDK 访问", "Bucket 权限最小化"], AMBER, 15)
    s.card(1438, 448, 402, 128, "数据保护", ["服务端加密 SSE（按现网）", "版本化 / 生命周期 / 防误删"], GREEN, 15)
    s.card(1438, 606, 402, 128, "访问控制", ["RAM / STS 临时凭证", "私网 Endpoint / HTTPS"], BLUE, 15)
    s.card(1438, 764, 402, 98, "备份归档", ["数据库备份落 OSS（建议策略）"], PURPLE, 14)

    # Data paths
    path_y = [318, 474, 630]
    for y in path_y:
        s.line(504, y, 560, y)
    s.line(1346, 335, 1402, 335, color=AMBER, arrow="amber")
    s.polyline([(1346, 790), (1380, 790), (1380, 813), (1430, 813)], color=PURPLE, arrow=None, dash="8 6")
    s.text(1357, 773, "备份 / 归档", 13, PURPLE, 700)

    s.rect(52, 928, 1816, 58, fill="#FFF7E6", stroke="#F3C677", rx=16, sw=1)
    s.text(960, 964, "关键边界：数据库不能因缺少 IP 信息而默认绑定至 8 个 K8s 节点；投产图需补齐实例地址、HA、备份与容灾参数。", 15, AMBER, 700, "middle")

    s.footer("存储技术清单来自原 PDF；OSS 为已采购服务；备份落 OSS 标注为建议，不代表现网已启用。")
    return s


def diagram_5() -> SVG:
    s = SVG(
        "⑤ 负载均衡组件：接入层 / 业务层 / 数据层",
        "按职责拆分公网入口、K8s 服务路由与数据客户端路由，避免把所有“负载”混为同一层",
        "05 / 05",
    )

    layers = [
        (52, 160, 1816, 222, "接入层", "公网流量接入、攻击防护、七层路由", BLUE, "#EEF5FD"),
        (52, 414, 1816, 250, "业务层", "服务发现、Pod 负载均衡、服务间调用与容错", CYAN, "#ECF9FA"),
        (52, 696, 1816, 250, "数据层", "数据库连接池、中间件客户端与存储端点路由", GREEN, "#EDF8F4"),
    ]
    for x, y, w, h, title, desc, color, fill in layers:
        s.rect(x, y, w, h, fill=fill, stroke=color, rx=20, sw=1.7)
        s.add(f'<rect x="{x}" y="{y}" width="176" height="{h}" rx="20" fill="{color}"/>')
        s.add(f'<rect x="{x + 150}" y="{y}" width="26" height="{h}" fill="{color}"/>')
        s.text(x + 88, y + 66, title, 27, WHITE, 700, "middle")
        s.multiline(x + 88, y + 101, desc.split("、"), 13, "#EAF3FB", 400, "middle", 1.45)

    # Access layer boxes
    access = [
        (260, "域名管理 / DNS", ["名称解析", "非负载均衡器"], PURPLE),
        (548, "DDoS + WAF", ["清洗与应用防护", "安全入口"], RED),
        (836, "阿里云 SLB", ["公网 VIP / 健康检查", "CLB/ALB 以现网为准"], BLUE),
        (1124, "K8s Ingress", ["Nginx / Ingress Controller", "七层路径路由"], CYAN),
        (1412, "统一网关", ["Spring Cloud Gateway", "鉴权 / 限流 / 路由"], PURPLE),
    ]
    for x, title, body, color in access:
        s.card(x, 210, 252, 120, title, body, color, 14)
    for x in [512, 800, 1088, 1376]:
        s.line(x + 4, 270, x + 28, 270)

    # Business layer
    business = [
        (260, "Nacos", ["服务注册 / 发现", "配置管理"], PURPLE),
        (548, "Kubernetes Service", ["ClusterIP", "转发至健康 Pod"], CYAN),
        (836, "Feign + Ribbon", ["服务间调用", "客户端负载均衡"], BLUE),
        (1124, "Sentinel", ["限流 / 熔断 / 降级", "不是负载均衡器"], AMBER),
        (1412, "业务 Pod 副本", ["Deployment / HPA", "跨 8 节点调度"], GREEN),
    ]
    for x, title, body, color in business:
        s.card(x, 482, 252, 124, title, body, color, 14)
    for x in [512, 800, 1088, 1376]:
        s.line(x + 4, 544, x + 28, 544, color=CYAN, arrow="green")

    # Data layer
    data = [
        (260, "数据库驱动 / 连接池", ["MySQL / MongoDB", "主备路由按现网"], GREEN),
        (548, "Redis 客户端", ["Cluster / Sentinel", "拓扑感知路由"], RED),
        (836, "RabbitMQ 客户端", ["连接多个节点", "Exchange / Queue"], AMBER),
        (1124, "ES 客户端", ["协调节点 / 节点发现", "分片路由"], PURPLE),
        (1412, "OSS Endpoint", ["SDK / HTTPS", "服务端高可用"], BLUE),
    ]
    for x, title, body, color in data:
        s.card(x, 764, 252, 124, title, body, color, 14)
    for x in [512, 800, 1088, 1376]:
        s.line(x + 4, 826, x + 28, 826, color=GREEN, arrow="green", dash="7 5")

    # Vertical relations
    for x in [962, 1250, 1538]:
        s.line(x, 382, x, 406, color=CYAN, arrow="green")
    for x in [386, 674, 962, 1250, 1538]:
        s.line(x, 664, x, 688, color=GREEN, arrow="green")

    s.rect(224, 962, 1644, 38, fill="#FFF7E6", stroke="#F3C677", rx=18, sw=1)
    s.text(1046, 987, "数据层通常由客户端、连接池或集群自身完成路由，不直接复用公网入口 SLB。", 14, AMBER, 700, "middle")

    s.footer("请求主链路：DNS → DDoS/WAF → SLB → Ingress → Gateway → K8s Service/Pod → 数据服务。")
    return s


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    diagrams = [
        ("01-服务器集群节点与网络分区.svg", diagram_1()),
        ("02-微服务模块分布.svg", diagram_2()),
        ("03-安全防护组件与等保控制.svg", diagram_3()),
        ("04-存储部署-OSS与数据库.svg", diagram_4()),
        ("05-负载均衡分层.svg", diagram_5()),
    ]
    for filename, diagram in diagrams:
        target = OUT_DIR / filename
        target.write_text(diagram.finish(), encoding="utf-8")
        print(target)


if __name__ == "__main__":
    main()
