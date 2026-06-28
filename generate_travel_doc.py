#!/usr/bin/env python3
"""Generate Word document for Xi'an & Chengdu family travel itinerary."""

import json
from pathlib import Path

from docx import Document
from docx.shared import Pt, Cm, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

from build_transport_data import build_transport_guides

FONT = "微软雅黑"
OUTPUT = Path("/workspace/广州-西安-成都亲子暑期旅行行程表.docx")
DESKTOP = Path("/home/ubuntu/Desktop/广州-西安-成都亲子暑期旅行行程表.docx")


def set_cell_shading(cell, color_hex):
    shading = OxmlElement("w:shd")
    shading.set(qn("w:fill"), color_hex)
    cell._tc.get_or_add_tcPr().append(shading)


def set_run_font(run, size=11, bold=False, color=None):
    run.font.name = FONT
    run._element.rPr.rFonts.set(qn("w:eastAsia"), FONT)
    run.font.size = Pt(size)
    run.font.bold = bold
    if color:
        run.font.color.rgb = RGBColor(*color)


def add_heading(doc, text, level=1):
    p = doc.add_paragraph()
    set_run_font(p.add_run(text), size={1: 18, 2: 14, 3: 12}.get(level, 12),
                 bold=True, color={1: (0x1A, 0x47, 0x7A), 2: (0x2E, 0x6D, 0xA4), 3: (0x44, 0x72, 0xC4)}.get(level))
    p.paragraph_format.space_before = Pt(12 if level > 1 else 6)
    p.paragraph_format.space_after = Pt(6)


def add_para(doc, text, size=10, bold=False, color=None):
    p = doc.add_paragraph()
    set_run_font(p.add_run(text), size=size, bold=bold, color=color)
    p.paragraph_format.space_after = Pt(4)


def add_bullet(doc, text, size=10):
    p = doc.add_paragraph(style="List Bullet")
    set_run_font(p.add_run(text), size=size)
    p.paragraph_format.space_after = Pt(2)


def add_day_section(doc, date_title, subtitle, items):
    add_heading(doc, date_title, level=2)
    add_para(doc, subtitle, color=(0x66, 0x66, 0x66))
    table = doc.add_table(rows=1, cols=2)
    table.style = "Table Grid"
    hdr = table.rows[0].cells
    hdr[0].text, hdr[1].text = "时间", "行程安排"
    for cell in hdr:
        for para in cell.paragraphs:
            set_run_font(para.runs[0], size=10, bold=True, color=(0xFF, 0xFF, 0xFF))
            para.alignment = WD_ALIGN_PARAGRAPH.CENTER
        set_cell_shading(cell, "2E6DA4")
    for time_slot, activity in items:
        row = table.add_row().cells
        row[0].text, row[1].text = time_slot, activity
        for i, cell in enumerate(row):
            for para in cell.paragraphs:
                set_run_font(para.runs[0], size=10, bold=(i == 0))
                if i == 0:
                    para.alignment = WD_ALIGN_PARAGRAPH.CENTER
    doc.add_paragraph()


def add_info_table(doc, headers, rows):
    table = doc.add_table(rows=1, cols=len(headers))
    table.style = "Table Grid"
    for i, h in enumerate(headers):
        table.rows[0].cells[i].text = h
        for para in table.rows[0].cells[i].paragraphs:
            set_run_font(para.runs[0], size=9, bold=True, color=(0xFF, 0xFF, 0xFF))
            para.alignment = WD_ALIGN_PARAGRAPH.CENTER
        set_cell_shading(table.rows[0].cells[i], "1A477A")
    for row_data in rows:
        row = table.add_row().cells
        for i, val in enumerate(row_data):
            row[i].text = val
            for para in row[i].paragraphs:
                set_run_font(para.runs[0], size=9)
    doc.add_paragraph()


def add_transport_route(doc, title, method, steps, estimate=None):
    add_heading(doc, title, level=3)
    add_para(doc, f"交通方式：{method}", bold=True, color=(0x2E, 0x6D, 0xA4))
    add_para(doc, "乘车步骤：", bold=True)
    for step in steps:
        add_bullet(doc, step)
    if estimate:
        add_para(doc, estimate, bold=True, color=(0xC0, 0x39, 0x2B))
    doc.add_paragraph()


def load_itinerary():
    days = []

    def day(date, theme, *items):
        days.append({"date": date, "theme": theme, "items": list(items)})

    day(
        "7月4日（周六）广州 → 西安", "抵达古都，机场至大雁塔酒店",
        ("09:55 - 12:35", "乘坐航班飞往西安咸阳机场。"),
        ("12:35 - 15:00", "【地铁】14号线→4号线：机场西站→西安北站→大雁塔站（详见第二部分，约2小时，9元/人）"),
        ("15:00 - 15:15", "大雁塔站C/D出口，沿慈恩西路步行700米入住雅缦东方庭院酒店。"),
        ("15:15 - 17:00", "大悦城下午茶，回房午休。"),
        ("17:00 - 18:00", "酒店庭院换汉服拍照。"),
        ("18:00 - 19:30", "【晚餐】长安大牌档（大悦城店）。推荐：葫芦鸡、金线油塔。"),
        ("19:45 - 21:30", "大唐不夜城：音乐喷泉、街头表演。"),
        ("21:30+", "步行回酒店。"),
    )
    day(
        "7月5日（周日）兵马俑、丽山园、世博园千古情", "秦风研学，高效避暑",
        ("07:30 - 08:30", "酒店早餐。"),
        ("08:30 - 10:10", "地铁3→1→9号线至华清池，打车至兵马俑（约1小时40分）"),
        ("10:10 - 12:30", "兵马俑一、二、三号坑深度研学。"),
        ("12:30 - 13:30", "免费摆渡至丽山园：铜车马、百戏俑坑、秦陵封土（建议15元电瓶车）。"),
        ("13:30 - 14:30", "【午餐】西安饭庄（临潼店）。推荐：温拌腰丝、糟肉。"),
        ("14:30 - 15:00", "打车至西安千古情景区（约25分钟，50-60元）。"),
        ("15:00 - 16:30", "世博园空调咖啡厅午休。"),
        ("16:30 - 19:30", "世博园+《西安千古情》（18:00场次）。"),
        ("19:30 - 20:15", "地铁3号线回大雁塔站。"),
        ("20:15 - 21:30", "【晚餐】醉长安（大雁塔店）。推荐：晾衣毛肚、蜂蜜凉糕。"),
        ("21:30+", "步行回酒店。"),
    )
    day(
        "7月6日（周一）华山一日征服", "西上西下，画舫夜游",
        ("07:00 - 07:30", "早餐，打包面包/能量棒/水果/矿泉水（不带肉夹馍）。"),
        ("07:30 - 08:15", "地铁4号线：大雁塔→西安北站。"),
        ("08:40 - 09:15", "高铁：西安北→华山北。"),
        ("09:20 - 09:35", "打车至华山游客中心。"),
        ("09:45 - 15:45", "西上西下：大巴→西峰索道→西峰+南峰→原路下山。"),
        ("15:45 - 17:00", "打车回华山北站候高铁。"),
        ("17:30 - 18:10", "高铁回西安北站。"),
        ("18:15 - 19:00", "地铁4号线回大雁塔站，洗澡换衣服。"),
        ("19:15 - 20:30", "【晚餐】陕九·老陕菜。推荐：臊子面、老豆腐、羊排。"),
        ("20:30 - 21:45", "大唐芙蓉园画舫夜游（有冷气）。"),
        ("21:45 - 22:00", "地铁回酒店。"),
    )
    day(
        "7月7日（周二）陕历博、大皮院、城墙", "历史博物馆，城墙晚风",
        ("09:30 - 10:30", "酒店早餐。"),
        ("10:30 - 12:30", "陕西历史博物馆（打车5分钟）。"),
        ("12:30 - 14:30", "【午餐】志亮灌汤蒸饺（大皮院）。地铁2→6号线至广济街。"),
        ("14:30 - 16:30", "回酒店午休。"),
        ("17:00 - 19:30", "西安城墙永宁门（地铁3→2号线，步行或电瓶车）。"),
        ("19:30 - 21:00", "【晚餐】西安饭庄（南门里店）。"),
        ("21:00+", "回酒店收拾行李。"),
    )
    day(
        "7月8日（周三）西安 → 成都", "老茶馆与锦江夜游",
        ("08:00 - 08:30", "退房。"),
        ("08:30 - 09:20", "地铁4号线至西安北站。"),
        ("10:00 - 14:00", "西成高铁至成都东。"),
        ("14:00 - 14:45", "地铁2号线至通惠门站，步行至温德姆酒店。"),
        ("15:00 - 16:30", "午休。"),
        ("16:30 - 18:15", "人民公园鹤鸣茶社（步行）：竹叶青、采耳、蛋烘糕。"),
        ("18:15 - 19:30", "【晚餐】饕林餐厅（奎星楼店）。"),
        ("19:30 - 21:00", "地铁至东门大桥，夜游锦江（东门码头）。"),
        ("21:00 - 21:30", "地铁回酒店。"),
    )
    day(
        "7月9日（周四）大熊猫、杜甫草堂、文殊坊", "萌熊猫，诗圣草堂，国潮大秀",
        ("07:00 - 07:45", "打车至熊猫基地南门（35分钟，45-50元）。"),
        ("07:45 - 11:15", "熊猫基地晨间游览（含花花）。"),
        ("11:15 - 13:00", "【午餐】盘飧市（春熙路店）。"),
        ("13:00 - 14:30", "地铁2号线回酒店午休。"),
        ("14:30 - 16:30", "杜甫草堂博物馆（打车10分钟）。"),
        ("16:30 - 18:30", "地铁4→1号线至文殊院，洞子口张老二凉粉（下午茶）。"),
        ("18:30 - 20:00", "文殊坊舒适川菜馆晚餐。"),
        ("20:00 - 21:30", "《花重锦官城》大秀（妙剧场）。"),
        ("21:30 - 22:00", "地铁回酒店。"),
    )
    day(
        "7月10日（周五）三星堆奇妙日", "古蜀文明，太古里",
        ("08:30 - 09:30", "早餐。"),
        ("09:30 - 11:00", "地铁2号线→成都东→广汉北→打车至三星堆。"),
        ("11:20 - 15:00", "三星堆新馆深度游，馆内简餐。"),
        ("15:00 - 16:30", "返回酒店。"),
        ("16:30 - 18:30", "休息。"),
        ("18:30 - 20:30", "【晚餐】柴门饭儿（太古里店）。"),
        ("20:30 - 21:30", "太古里、IFS大熊猫。"),
        ("21:30+", "地铁回酒店。"),
    )
    day(
        "7月11日（周六）都江堰与熊猫谷", "同台换乘，水利奇观",
        ("08:00 - 09:30", "地铁2号线→犀浦，同台换乘城铁→都江堰。"),
        ("09:30 - 12:00", "熊猫谷（红熊猫放养区可能排队）。"),
        ("12:00 - 13:30", "【午餐】钟鸭子（都江堰总店）。"),
        ("13:30 - 16:00", "秦堰楼6号门进，顺坡下行游览都江堰。"),
        ("16:00 - 18:00", "离堆公园站→犀浦→地铁回酒店。"),
        ("18:30 - 21:00", "【告别晚餐】听香·新派川菜（宽窄巷子店）。"),
        ("21:00+", "整理行李。"),
    )
    day(
        "7月12日（周日）成都 → 惠州", "双机场返程",
        ("09:00 - 10:30", "早餐，退房。"),
        ("10:30 - 11:30", "A.双流机场—打车约40-50元；B.天府机场—地铁18号线大站快车。"),
        ("11:30 - 13:30", "值机，飞返惠州。"),
    )

    cp = "6周岁以下（不占座）免费；\n6-14周岁半价；\n14周岁及以上成人票。"
    sections = [
        {
            "title": "一、提前 15 天（大交通：高铁票）",
            "note": "请在「铁路12306」APP定闹钟抢票。",
            "headers": ["出行日期", "路线及车次建议", "预约/抢票时间", "购票平台", "儿童政策"],
            "rows": [
                ["7月6日", "西安北⇄华山北\n去08:20-08:50 返17:30-18:00", "提前15天12:30", "12306", cp],
                ["7月8日", "西安北→成都东\n10:00-14:00", "提前15天12:30", "12306", "同上"],
                ["7月10日", "成都东⇄广汉北\n去10:00-10:40 返15:00-15:40", "提前15天12:30", "12306", "同上"],
                ["7月11日", "犀浦→都江堰/离堆公园→犀浦", "提前15天12:30", "12306", "同上"],
            ],
        },
        {
            "title": "二、核心景点门票（需严格控时抢购）",
            "headers": ["景点名称", "参观日期", "开放预约时间", "预约/购票渠道", "票价及儿童政策", "核心提示"],
            "rows": [
                ["秦始皇兵马俑\n（含丽山园）", "7月5日", "提前7天\n10:00放票", "微信【秦始皇帝陵博物院】", "成人120元；16岁及以下免费", "10:00-12:00入园；两园一票制"],
                ["陕西历史博物馆", "7月7日", "提前5-7天", "微信【陕西历史博物馆】", "基本陈列免费，实名预约", "暑期极难抢！"],
                ["大熊猫繁育基地", "7月9日", "提前7-14天", "微信【成都大熊猫繁育研究基地】", "成人55元；6岁或1.3m以下免票", "必须预约上午票"],
                ["杜甫草堂博物馆", "7月9日", "提前3-7天", "微信【杜甫草堂博物馆】", "成人50元；6-18岁半价", "下午参观可避暑"],
                ["三星堆博物馆", "7月10日", "提前5天\n20:00放票", "微信【三星堆博物馆】", "成人72元；未满6岁免票", "暑期最难抢！20:00抢下午场"],
                ["都江堰熊猫谷", "7月11日", "提前7-14天", "微信【熊猫谷】", "成人55元；6岁及以下免票", "红熊猫放养区二次排队"],
                ["都江堰景区", "7月11日", "提前7天内", "微信【青城山都江堰】", "成人80元；14岁以下免票", "秦堰楼6号门进"],
            ],
        },
        {
            "title": "三、演艺、特色体验与夜游票",
            "headers": ["体验项目", "体验日期", "建议预约时间", "抢票平台", "核心注意事项"],
            "rows": [
                ["《西安千古情》", "7月5日", "提前7-10天", "携程/美团", "18:00场次，含世博园"],
                ["华山门票及索道", "7月6日", "提前3-5天", "微信【华山景区】", "西上西下套票"],
                ["大唐芙蓉园画舫", "7月6日", "提前1-2天", "微信【大唐芙蓉园】", "门票+画舫套票"],
                ["西安古城墙电瓶车", "7月7日", "现场购买", "永宁门", "代替儿童骑行"],
                ["夜游锦江", "7月8日", "提前5-7天", "微信【夜游锦江】", "东门码头出发"],
                ["《花重锦官城》", "7月9日", "提前5天", "携程/美团", "妙剧场20:00场次"],
            ],
        },
    ]
    return days, sections


def main():
    days, sections = load_itinerary()
    transport_guides = build_transport_guides()

    doc = Document()
    for sec in doc.sections:
        sec.top_margin = Cm(2)
        sec.bottom_margin = Cm(2)
        sec.left_margin = Cm(2.5)
        sec.right_margin = Cm(2.5)

    t = doc.add_paragraph()
    t.alignment = WD_ALIGN_PARAGRAPH.CENTER
    set_run_font(t.add_run("广州 → 西安 → 成都 亲子暑期旅行行程表"), size=22, bold=True, color=(0x1A, 0x47, 0x7A))
    s = doc.add_paragraph()
    s.alignment = WD_ALIGN_PARAGRAPH.CENTER
    set_run_font(s.add_run("2025年7月4日—7月12日 | 完整行程 + 详细交通指南 + 门票预约清单"), size=11, color=(0x66, 0x66, 0x66))
    s.paragraph_format.space_after = Pt(18)

    add_heading(doc, "第一部分：完整行程表（更新版）", level=1)
    for d in days:
        add_day_section(doc, d["date"], d["theme"], d["items"])

    doc.add_page_break()
    add_heading(doc, "第二部分：详细交通指南", level=1)
    add_para(doc, "以下为每日逐段交通路线，含地铁换乘、打车定位、步行方向及预估时间与费用。")
    for g in transport_guides:
        add_heading(doc, g["date"], level=2)
        for route in g["routes"]:
            add_transport_route(doc, route["title"], route["method"], route["steps"], route.get("estimate"))

    doc.add_page_break()
    add_heading(doc, "第三部分：要买和预约的门票/车票清单", level=1)
    add_para(doc, "暑假（7月）旺季，大部分门票须提前定闹钟抢购。")
    for sec in sections:
        add_heading(doc, sec["title"], level=2)
        if sec.get("note"):
            add_para(doc, sec["note"], bold=True, color=(0xC0, 0x39, 0x2B))
        add_info_table(doc, sec["headers"], sec["rows"])

    note = doc.add_paragraph()
    note.alignment = WD_ALIGN_PARAGRAPH.CENTER
    set_run_font(note.add_run("— 祝您旅途愉快，阖家安康 —"), size=10, color=(0x99, 0x99, 0x99))

    doc.save(OUTPUT)
    doc.save(DESKTOP)
    print(f"已生成: {OUTPUT}")
    print(f"已复制: {DESKTOP}")


if __name__ == "__main__":
    main()
