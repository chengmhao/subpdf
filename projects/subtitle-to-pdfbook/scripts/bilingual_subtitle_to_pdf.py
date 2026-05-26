#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
双语字幕转PDF台词本工具

功能：
- 支持SRT、VTT、ASS字幕格式
- 生成A4纸张大小PDF（210mm × 297mm）
- 表格形式展示，两列布局
- 左字幕1，右字幕2
- 自动分页，保持阅读流畅
- 自动检测系统中文字体
- 支持英语单词高亮（按难度等级包含更高难度词汇）

词汇难度等级（从低到高）：
Level 1: 四级 (CET4)
Level 2: 六级 (CET6) = 专四 (TEM4)
Level 3: 专八 (TEM8) = 考研 (Kaoyan)
Level 4: 雅思 (IELTS) = 托福 (TOEFL)
Level 5: GMAT = GRE = SAT

高亮规则：
1. 选择某个等级时，自动包含该等级及更高等级的词汇
2. 分类高亮：热门单词、大学单词、出国单词
"""

import argparse
import platform
import re
import sys
from pathlib import Path
from typing import List, Tuple, Optional, Set, Dict

# 字幕解析
try:
    import srt
except ImportError:
    srt = None

try:
    import webvtt
except ImportError:
    webvtt = None

try:
    import ass
except ImportError:
    ass = None

# PDF生成
try:
    from reportlab.lib import colors
    from reportlab.lib.pagesizes import mm, inch, A4
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.units import cm
    from reportlab.platypus import SimpleDocTemplate, BaseDocTemplate, PageTemplate, Frame, Table, TableStyle, Paragraph, Spacer, PageBreak
    from reportlab.pdfbase import pdfmetrics
    from reportlab.pdfbase.ttfonts import TTFont
except ImportError:
    print("错误：缺少reportlab库，请运行: pip install reportlab==4.0.7")
    sys.exit(1)


# 语言检测映射表
LANGUAGE_NAMES = {
    'zh': '中文',
    'en': 'English',
    'es': 'Español',
    'fr': 'Français',
    'de': 'Deutsch',
    'ja': '日本語',
    'ko': '한국어',
    'pt': 'Português',
    'ru': 'Русский',
    'it': 'Italiano',
    'ar': 'العربية',
    'th': 'ไทย',
    'vi': 'Tiếng Việt',
    'nl': 'Nederlands',
    'pl': 'Polski',
    'tr': 'Türkçe',
    'id': 'Bahasa Indonesia',
    'ms': 'Bahasa Melayu',
}


def detect_language(text: str) -> str:
    """
    检测文本语言
    
    参数:
        text: 文本内容
    
    返回:
        语言代码，如 'zh', 'en', 'es' 等
    """
    if not text:
        return 'en'
    
    # 统计不同字符类型的比例
    chinese_chars = len(re.findall(r'[\u4e00-\u9fff]', text))
    japanese_chars = len(re.findall(r'[\u3040-\u309f\u30a0-\u30ff]', text))
    korean_chars = len(re.findall(r'[\uac00-\ud7af]', text))
    arabic_chars = len(re.findall(r'[\u0600-\u06ff]', text))
    thai_chars = len(re.findall(r'[\u0e00-\u0e7f]', text))
    cyrillic_chars = len(re.findall(r'[\u0400-\u04ff]', text))
    
    total_chars = len(text.replace(' ', ''))
    if total_chars == 0:
        total_chars = 1
    
    # 根据字符比例判断语言
    chinese_ratio = chinese_chars / total_chars
    japanese_ratio = japanese_chars / total_chars
    korean_ratio = korean_chars / total_chars
    arabic_ratio = arabic_chars / total_chars
    thai_ratio = thai_chars / total_chars
    cyrillic_ratio = cyrillic_chars / total_chars
    
    if chinese_ratio > 0.1:
        return 'zh'
    elif japanese_ratio > 0.05:
        return 'ja'
    elif korean_ratio > 0.05:
        return 'ko'
    elif arabic_ratio > 0.05:
        return 'ar'
    elif thai_ratio > 0.05:
        return 'th'
    elif cyrillic_ratio > 0.1:
        return 'ru'
    
    # 检测拉丁字母语言（通过常见词汇）
    text_lower = text.lower()
    
    # 英语特征词（优先检测）
    en_words = ['the', 'is', 'are', 'was', 'were', 'have', 'has', 'had', 'will', 'would', 
                'can', 'could', 'should', 'may', 'might', 'must', 'this', 'that', 'these',
                'those', 'what', 'which', 'who', 'when', 'where', 'why', 'how', 'not', 'but']
    en_count = len(re.findall(r'\b(' + '|'.join(en_words) + r')\b', text_lower))
    
    # 西班牙语特征（排除与英语重叠的词）
    es_words = ['el', 'los', 'las', 'que', 'y', 'una', 'por', 'con', 'para', 'muy', 'tengo', 'tiene']
    es_count = len(re.findall(r'\b(' + '|'.join(es_words) + r')\b', text_lower))
    
    # 法语特征
    fr_words = ['le', 'les', 'du', 'des', 'est', 'une', 'dans', 'avec', 'vous', 'nous', 'je', 'tu']
    fr_count = len(re.findall(r'\b(' + '|'.join(fr_words) + r')\b', text_lower))
    
    # 德语特征
    de_words = ['der', 'die', 'das', 'und', 'ist', 'eine', 'den', 'von', 'mit', 'für', 'ich', 'du']
    de_count = len(re.findall(r'\b(' + '|'.join(de_words) + r')\b', text_lower))
    
    # 葡萄牙语特征
    pt_words = ['os', 'que', 'do', 'da', 'em', 'uma', 'para', 'com', 'você', 'não', 'sou']
    pt_count = len(re.findall(r'\b(' + '|'.join(pt_words) + r')\b', text_lower))
    
    # 意大利语特征
    it_words = ['il', 'lo', 'di', 'che', 'una', 'per', 'con', 'sono', 'essere', 'hanno']
    it_count = len(re.findall(r'\b(' + '|'.join(it_words) + r')\b', text_lower))
    
    # 找出得分最高的语言
    scores = {
        'en': en_count,
        'es': es_count,
        'fr': fr_count,
        'de': de_count,
        'pt': pt_count,
        'it': it_count
    }
    
    max_lang = max(scores, key=scores.get)
    if scores[max_lang] > 2:
        return max_lang
    
    # 默认英语
    return 'en'


def get_language_name(lang_code: str) -> str:
    """
    根据语言代码获取语言显示名称
    
    参数:
        lang_code: 语言代码
    
    返回:
        语言显示名称
    """
    return LANGUAGE_NAMES.get(lang_code, lang_code.upper())


def format_timestamp(seconds: float) -> str:
    """
    将秒数格式化为时间轴字符串
    
    参数:
        seconds: 秒数
    
    返回:
        格式化的时间轴，如 "01:30:45" 或 "30:45"（小于1小时不显示小时）
    """
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    
    if hours > 0:
        return f"{hours:02d}:{minutes:02d}:{secs:02d}"
    else:
        return f"{minutes:02d}:{secs:02d}"


# 词汇难度等级定义（从低到高）
WORD_LEVELS = {
    'cet4': 1,      # 四级
    'cet6': 2,      # 六级
    'tem4': 2,      # 专四（与六级同级）
    'tem8': 3,      # 专八
    'kaoyan': 3,    # 考研（与专八同级）
    'ielts': 4,     # 雅思
    'toefl': 4,     # 托福（与雅思同级）
    'gmat': 5,      # GMAT
    'gre': 5,       # GRE（与GMAT同级）
    'sat': 5,       # SAT（与GMAT同级）
}

# 分类高亮定义
HIGHLIGHT_CATEGORIES = {
    'hot': ['cet4', 'cet6', 'kaoyan'],  # 热门单词：四级、六级、考研
    'college': ['cet4', 'cet6', 'kaoyan', 'tem4', 'tem8'],  # 大学单词：四级、六级、考研、专四、专八
    'abroad': ['ielts', 'toefl', 'gmat', 'gre', 'sat'],  # 出国单词：雅思、托福、GMAT、GRE、SAT
}


class SubtitleEntry:
    """字幕条目类"""
    def __init__(self, index: int, start_time: float, end_time: float, content: str):
        self.index = index
        self.start_time = start_time
        self.end_time = end_time
        self.content = content.strip()
    
    def __repr__(self):
        return f"SubtitleEntry({self.index}, {self.start_time:.2f}s-{self.end_time:.2f}s, '{self.content[:20]}...')"


def clean_subtitle_text(text: str) -> str:
    """
    清理字幕文本中的标签和特殊符号
    支持清理: <i>, </i>, <b>, </b>, <u>, </u>, <font ...>, {\\an8}, {\\pos} 等ASS/SSA标签
    """
    # 清理HTML样式标签: <i>, </i>, <b>, </b>, <u>, </u>, <font ...>, </font>
    text = re.sub(r'</?[iIbBuU]>', '', text)
    text = re.sub(r'</?[fF][oO][nN][tT][^>]*>', '', text)
    
    # 清理ASS/SSA样式标签: {\an8}, {\pos(x,y)}, {\b1}, {\i1}, {\u1}, {\b0}, {\i0}, {\u0} 等
    text = re.sub(r'\{\\[^}]*\}', '', text)
    
    # 清理其他常见标签: <c.magenta>, </c>, {\k...}, {\K...}
    text = re.sub(r'</?c(\.[^>]*)?>', '', text)
    text = re.sub(r'\{\\[kK][^}]*\}', '', text)
    
    # 清理多余空白字符
    text = re.sub(r'\s+', ' ', text).strip()
    
    return text


def parse_srt(file_path: str) -> List[SubtitleEntry]:
    """解析SRT格式字幕"""
    if srt is None:
        raise ImportError("缺少srt库，请运行: pip install srt==3.5.3")
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    subtitles = list(srt.parse(content))
    entries = []
    for idx, sub in enumerate(subtitles, 1):
        start = sub.start.total_seconds()
        end = sub.end.total_seconds()
        text = clean_subtitle_text(sub.content)
        if text:
            entries.append(SubtitleEntry(idx, start, end, text))
    
    return entries


def parse_vtt(file_path: str) -> List[SubtitleEntry]:
    """解析VTT格式字幕"""
    if webvtt is None:
        raise ImportError("缺少webvtt库，请运行: pip install webvtt-py==0.4.6")
    
    vtt = webvtt.read(file_path)
    entries = []
    for idx, caption in enumerate(vtt.captions, 1):
        start_str = caption.start
        end_str = caption.end
        
        def parse_vtt_time(time_str: str) -> float:
            parts = time_str.split(':')
            if len(parts) == 3:
                h, m, s = parts
                return int(h) * 3600 + int(m) * 60 + float(s)
            elif len(parts) == 2:
                m, s = parts
                return int(m) * 60 + float(s)
            return 0.0
        
        start = parse_vtt_time(start_str)
        end = parse_vtt_time(end_str)
        text = clean_subtitle_text(caption.text)
        if text:
            entries.append(SubtitleEntry(idx, start, end, text))
    
    return entries


def parse_ass(file_path: str) -> List[SubtitleEntry]:
    """解析ASS/SSA格式字幕"""
    if ass is None:
        raise ImportError("缺少ass库，请运行: pip install ass==0.5.2")
    
    with open(file_path, 'r', encoding='utf-8') as f:
        doc = ass.parse(f)
    
    entries = []
    idx = 1
    for event in doc.events:
        if isinstance(event, ass.document.Dialogue):
            start = event.start.total_seconds()
            end = event.end.total_seconds()
            text = re.sub(r'\{[^}]*\}', '', event.text)
            text = text.replace('\\N', '\n')
            text = clean_subtitle_text(text)
            if text:
                entries.append(SubtitleEntry(idx, start, end, text))
                idx += 1
    
    return entries


def parse_subtitle(file_path: str) -> List[SubtitleEntry]:
    """自动识别并解析字幕文件"""
    path = Path(file_path)
    ext = path.suffix.lower()
    
    if ext == '.srt':
        return parse_srt(file_path)
    elif ext == '.vtt':
        return parse_vtt(file_path)
    elif ext in ['.ass', '.ssa']:
        return parse_ass(file_path)
    else:
        raise ValueError(f"不支持的字幕格式: {ext}，支持的格式: SRT, VTT, ASS")


def align_subtitles(subs1: List[SubtitleEntry], subs2: List[SubtitleEntry]) -> List[Tuple[SubtitleEntry, SubtitleEntry]]:
    """对齐两个字幕列表"""
    aligned = []
    i, j = 0, 0
    
    while i < len(subs1) and j < len(subs2):
        s1, s2 = subs1[i], subs2[j]
        
        overlap_start = max(s1.start_time, s2.start_time)
        overlap_end = min(s1.end_time, s2.end_time)
        
        if overlap_start < overlap_end:
            aligned.append((s1, s2))
            i += 1
            j += 1
        elif s1.end_time < s2.start_time:
            aligned.append((s1, None))
            i += 1
        else:
            aligned.append((None, s2))
            j += 1
    
    while i < len(subs1):
        aligned.append((subs1[i], None))
        i += 1
    
    while j < len(subs2):
        aligned.append((None, subs2[j]))
        j += 1
    
    return aligned


def find_chinese_font() -> Optional[str]:
    """自动检测系统中的中文字体"""
    system = platform.system()
    
    font_candidates = []
    
    if system == "Linux":
        font_candidates = [
            "/usr/share/fonts/truetype/wqy/wqy-microhei.ttc",
            "/usr/share/fonts/wqy-microhei/wqy-microhei.ttc",
            "/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc",
            "/usr/share/fonts/wqy-zenhei/wqy-zenhei.ttc",
            "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc",
            "/usr/share/fonts/google-noto-cjk/NotoSansCJK-Regular.ttc",
            "/usr/share/fonts/noto-cjk/NotoSansCJK-Regular.ttc",
            "/usr/share/fonts/truetype/source-han/SourceHanSansCN-Regular.ttf",
            "/usr/share/fonts/adobe-source-han-sans/SourceHanSansCN-Regular.ttf",
            "/usr/share/fonts/truetype/droid/DroidSansFallbackFull.ttf",
            "/usr/share/fonts/truetype/arphic/uming.ttc",
            "/usr/share/fonts/truetype/arphic/ukai.ttc",
        ]
    elif system == "Darwin":
        font_candidates = [
            "/System/Library/Fonts/PingFang.ttc",
            "/System/Library/Fonts/STHeiti Light.ttc",
            "/System/Library/Fonts/Hiragino Sans GB.ttc",
            "/Library/Fonts/Arial Unicode.ttf",
        ]
    elif system == "Windows":
        font_candidates = [
            "C:/Windows/Fonts/msyh.ttc",
            "C:/Windows/Fonts/simhei.ttf",
            "C:/Windows/Fonts/simsun.ttc",
            "C:/Windows/Fonts/simkai.ttf",
        ]
    
    for font_path in font_candidates:
        if Path(font_path).exists():
            return font_path
    
    if system == "Linux":
        try:
            import subprocess
            result = subprocess.run(
                ["fc-list", ":lang=zh", "file"],
                capture_output=True, text=True, timeout=5
            )
            if result.returncode == 0 and result.stdout.strip():
                lines = result.stdout.strip().split('\n')
                if lines:
                    return lines[0].strip().split(':')[0]
        except Exception:
            pass
    
    return None


def register_chinese_font(font_path: str, font_name: str = "ChineseFont") -> str:
    """注册中文字体"""
    try:
        path = Path(font_path)
        
        if not path.exists():
            raise FileNotFoundError(f"字体文件不存在: {font_path}")
        
        if path.suffix.lower() == '.ttc':
            try:
                pdfmetrics.registerFont(TTFont(font_name, str(path), subfontIndex=0))
                return font_name
            except Exception:
                pdfmetrics.registerFont(TTFont(font_name, str(path)))
                return font_name
        else:
            pdfmetrics.registerFont(TTFont(font_name, str(path)))
            return font_name
    
    except Exception as e:
        raise RuntimeError(f"字体注册失败 ({font_path}): {e}")


def get_page_size() -> Tuple[float, float]:
    """获取A4纸张大小"""
    width = 210 * mm
    height = 297 * mm
    return (width, height)


def load_words_from_file(file_path: Path) -> Set[str]:
    """从文件加载词汇"""
    if not file_path.exists():
        print(f"警告：词汇文件不存在: {file_path}")
        return set(), {}
    
    words = set()
    definitions = {}  # 单词到释义的映射
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            
            # 支持两种格式：
            # 1. 纯单词：word
            # 2. 带释义：word\t词性\t释义 或 word 释义
            if '\t' in line:
                parts = line.split('\t')
                word = parts[0].strip().lower()
                definition = parts[2].strip() if len(parts) > 2 else (parts[1].strip() if len(parts) > 1 else '')
            elif ' ' in line and not line.startswith(' '):
                parts = line.split(None, 1)
                word = parts[0].strip().lower()
                definition = parts[1].strip() if len(parts) > 1 else ''
            else:
                word = line.lower()
                definition = ''
            
            if word:
                words.add(word)
                if definition:
                    # 只保留第一个释义，避免重复
                    if word not in definitions:
                        definitions[word] = definition
    
    return words, definitions


def load_definitions(skill_dir: Path) -> Dict[str, str]:
    """
    加载合并的释义文件
    
    返回:
        释义字典：key为单词，value为释义
    """
    definitions_file = skill_dir / "references" / "all_words_with_def.txt"
    definitions = {}
    
    if definitions_file.exists():
        with open(definitions_file, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith('#'):
                    continue
                if '\t' in line:
                    parts = line.split('\t', 1)
                    word = parts[0].strip().lower()
                    defn = parts[1].strip() if len(parts) > 1 else ''
                    if word and defn:
                        definitions[word] = defn
        print(f"已加载 {len(definitions)} 个单词释义")
    
    return definitions


def load_all_vocab_files(skill_dir: Path) -> Tuple[Dict[str, Set[str]], Dict[str, str]]:
    """
    加载所有词汇文件
    
    返回:
        (词汇字典, 释义字典)
        词汇字典：key为词汇类型，value为词汇集合
        释义字典：key为单词，value为释义
    """
    vocab_files = {
        'cet4': skill_dir / "references" / "cet4_words.txt",
        'cet6': skill_dir / "references" / "cet6_words.txt",
        'tem4': skill_dir / "references" / "tem4_words.txt",
        'tem8': skill_dir / "references" / "tem8_words.txt",
        'kaoyan': skill_dir / "references" / "kaoyan_words.txt",
        'ielts': skill_dir / "references" / "ielts_words.txt",
        'toefl': skill_dir / "references" / "toefl_words.txt",
        'gmat': skill_dir / "references" / "gmat_words.txt",
        'gre': skill_dir / "references" / "gre_words.txt",
        'sat': skill_dir / "references" / "sat_words.txt",
    }
    
    vocab_dict = {}
    
    for vocab_type, file_path in vocab_files.items():
        words, _ = load_words_from_file(file_path)
        if words:
            vocab_dict[vocab_type] = words
            print(f"已加载 {len(words)} 个 {vocab_type.upper()} 词汇")
    
    # 加载合并的释义文件
    all_definitions = load_definitions(skill_dir)
    
    return vocab_dict, all_definitions


def get_highlight_words_by_level(
    min_level: int,
    vocab_dict: Dict[str, Set[str]]
) -> Set[str]:
    """
    根据难度等级获取需要高亮的词汇
    
    参数:
        min_level: 最低难度等级（包含该等级及更高等级的词汇）
        vocab_dict: 词汇字典
    
    返回:
        需要高亮的词汇集合
    """
    highlight_words = set()
    
    for vocab_type, level in WORD_LEVELS.items():
        if level >= min_level and vocab_type in vocab_dict:
            highlight_words.update(vocab_dict[vocab_type])
    
    return highlight_words


def get_highlight_words_by_category(
    category: str,
    vocab_dict: Dict[str, Set[str]]
) -> Set[str]:
    """
    根据分类获取需要高亮的词汇
    
    参数:
        category: 分类名称（hot/college/abroad）
        vocab_dict: 词汇字典
    
    返回:
        需要高亮的词汇集合
    """
    highlight_words = set()
    
    if category not in HIGHLIGHT_CATEGORIES:
        print(f"警告：未知的分类: {category}")
        return highlight_words
    
    vocab_types = HIGHLIGHT_CATEGORIES[category]
    for vocab_type in vocab_types:
        if vocab_type in vocab_dict:
            highlight_words.update(vocab_dict[vocab_type])
    
    return highlight_words


def load_custom_words(words_input: str) -> Set[str]:
    """加载自定义高亮词汇"""
    words = set()
    
    if Path(words_input).exists():
        with open(words_input, 'r', encoding='utf-8') as f:
            for line in f:
                word = line.strip().lower()
                if word and not word.startswith('#'):
                    words.add(word)
        print(f"从文件加载 {len(words)} 个自定义词汇: {words_input}")
    else:
        for word in words_input.split(','):
            word = word.strip().lower()
            if word:
                words.add(word)
        print(f"加载 {len(words)} 个自定义词汇")
    
    return words


def highlight_words_in_text(
    text: str,
    highlight_words: Set[str],
    text_color: str = "#631511",
    bg_color: str = None,
    bold: bool = False,
    underline: bool = False,
    style_config: Dict = None
) -> Tuple[str, Set[str]]:
    """
    在文本中高亮指定单词
    
    参数:
        text: 原文本
        highlight_words: 高亮词汇集合
        text_color: 文字颜色（十六进制，如 #631511）
        bg_color: 背景颜色（可选，十六进制，如 #FFFF00）
        bold: 是否加粗
        underline: 是否下划线
        style_config: 完整样式配置（来自CSS，优先级高于单独参数）
    
    返回:
        (处理后的文本, 本行发现的高亮单词集合)
    """
    if not highlight_words:
        return text, set()
    
    found_words = set()
    
    text = text.replace('&', '&amp;')
    text = text.replace('<br/>', '\n')
    text = text.replace('<', '&lt;')
    text = text.replace('>', '&gt;')
    text = text.replace('\n', '<br/>')
    
    def replace_word(match):
        word = match.group(0)
        word_lower = word.lower()
        if word_lower in highlight_words:
            found_words.add(word_lower)
            
            # 使用CSS样式配置（优先）
            if style_config:
                return apply_style_to_text(word, style_config)
            
            # 传统方式：构建样式字符串
            style_parts = []
            style_parts.append(f'color="{text_color}"')
            if bg_color:
                style_parts.append(f'backColor="{bg_color}"')
            style_str = ' '.join(style_parts)
            
            # 构建标签
            open_tags = []
            close_tags = []
            
            if bold:
                open_tags.append('<b>')
                close_tags.insert(0, '</b>')
            if underline:
                open_tags.append('<u>')
                close_tags.insert(0, '</u>')
            
            open_tags.append(f'<font {style_str}>')
            close_tags.insert(0, '</font>')
            
            return ''.join(open_tags) + word + ''.join(close_tags)
        return word
    
    result = re.sub(r"[a-zA-Z]+(?:'[a-zA-Z]+)?", replace_word, text)
    
    return result, found_words


def parse_css_style(css_str: str) -> Dict:
    """
    解析CSS样式字符串为字典
    
    参数:
        css_str: CSS样式字符串，如 "color: #FF0000; font-size: 12px; font-weight: bold;"
    
    返回:
        样式字典，如 {'color': '#FF0000', 'font-size': '12px', 'font-weight': 'bold'}
    """
    if not css_str:
        return {}
    
    styles = {}
    # 移除注释
    css_str = re.sub(r'/\*.*?\*/', '', css_str, flags=re.DOTALL)
    
    for part in css_str.split(';'):
        part = part.strip()
        if ':' in part:
            key, value = part.split(':', 1)
            key = key.strip().lower()
            value = value.strip()
            if key and value:
                styles[key] = value
    
    return styles


def parse_css_file(css_path: str) -> Dict[str, Dict]:
    """
    解析CSS文件，返回选择器到样式的映射
    
    参数:
        css_path: CSS文件路径
    
    返回:
        字典，如 {'highlight-word': {...}, 'definition-word': {...}, ...}
    """
    try:
        with open(css_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        print(f"警告：无法读取CSS文件 {css_path}: {e}")
        return {}
    
    result = {}
    
    # 移除注释
    content = re.sub(r'/\*.*?\*/', '', content, flags=re.DOTALL)
    
    # 匹配选择器和样式块
    pattern = r'([^{]+)\{([^}]+)\}'
    for match in re.finditer(pattern, content):
        selectors = match.group(1).strip()
        style_block = match.group(2).strip()
        
        styles = parse_css_style(style_block)
        
        # 支持多个选择器（用逗号分隔）
        for selector in selectors.split(','):
            selector = selector.strip().lstrip('.')  # 移除前导点号
            if selector and styles:
                result[selector] = styles
    
    return result


def css_to_reportlab_style(css_styles: Dict, font_name: str = "Helvetica") -> Dict:
    """
    将CSS样式转换为reportlab兼容的样式参数
    
    参数:
        css_styles: CSS样式字典
        font_name: 字体名称
    
    返回:
        reportlab样式字典
    """
    result = {
        'color': None,
        'bg_color': None,
        'font_size': None,
        'bold': False,
        'italic': False,
        'underline': False,
        'font_name': font_name,
    }
    
    # 颜色
    if 'color' in css_styles:
        result['color'] = normalize_color(css_styles['color'])
    
    # 背景颜色
    bg_keys = ['background-color', 'background']
    for key in bg_keys:
        if key in css_styles:
            result['bg_color'] = normalize_color(css_styles[key])
            break
    
    # 字体大小
    if 'font-size' in css_styles:
        size_str = css_styles['font-size']
        # 解析大小（支持px, pt, em）
        size_match = re.match(r'(\d+(?:\.\d+)?)\s*(px|pt|em)?', size_str)
        if size_match:
            size = float(size_match.group(1))
            unit = size_match.group(2) or 'pt'
            if unit == 'px':
                size = size * 0.75  # px转pt
            elif unit == 'em':
                size = size * 12  # em转pt（假设基准12pt）
            result['font_size'] = int(size)
    
    # 字重
    if 'font-weight' in css_styles:
        weight = css_styles['font-weight'].lower()
        if weight in ['bold', 'bolder', '700', '800', '900']:
            result['bold'] = True
    
    # 字体样式
    if 'font-style' in css_styles:
        style = css_styles['font-style'].lower()
        if style == 'italic':
            result['italic'] = True
    
    # 文本装饰
    if 'text-decoration' in css_styles:
        decoration = css_styles['text-decoration'].lower()
        if 'underline' in decoration:
            result['underline'] = True
    
    # 边框（用于背景框效果）
    if 'border' in css_styles or 'border-radius' in css_styles:
        border = css_styles.get('border', '')
        radius = css_styles.get('border-radius', '0')
        result['border'] = border
        result['border_radius'] = radius
    
    # 内边距
    if 'padding' in css_styles:
        padding = css_styles['padding']
        result['padding'] = padding
    
    return result


def normalize_color(color_str: str) -> str:
    """
    标准化颜色值为十六进制格式
    
    支持格式：
    - 十六进制：#RGB, #RRGGBB, #RRGGBBAA
    - RGB函数：rgb(r, g, b), rgba(r, g, b, a)
    - 颜色名称：red, blue, green 等
    """
    if not color_str:
        return None
    
    color_str = color_str.strip().lower()
    
    # 已经是十六进制格式
    if color_str.startswith('#'):
        # #RGB -> #RRGGBB
        if len(color_str) == 4:
            return f"#{color_str[1]*2}{color_str[2]*2}{color_str[3]*2}"
        # #RRGGBB 或 #RRGGBBAA
        elif len(color_str) in [7, 9]:
            return color_str[:7].upper()
    
    # RGB函数
    rgb_match = re.match(r'rgba?\s*\(\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)', color_str)
    if rgb_match:
        r = int(rgb_match.group(1))
        g = int(rgb_match.group(2))
        b = int(rgb_match.group(3))
        return f"#{r:02X}{g:02X}{b:02X}"
    
    # 颜色名称映射
    color_names = {
        'red': '#FF0000',
        'green': '#008000',
        'blue': '#0000FF',
        'yellow': '#FFFF00',
        'orange': '#FFA500',
        'purple': '#800080',
        'pink': '#FFC0CB',
        'black': '#000000',
        'white': '#FFFFFF',
        'gray': '#808080',
        'grey': '#808080',
        'cyan': '#00FFFF',
        'magenta': '#FF00FF',
        'brown': '#A52A2A',
        'gold': '#FFD700',
        'silver': '#C0C0C0',
        'navy': '#000080',
        'teal': '#008080',
        'olive': '#808000',
        'maroon': '#800000',
        'aqua': '#00FFFF',
        'lime': '#00FF00',
        'coral': '#FF7F50',
        'crimson': '#DC143C',
        'salmon': '#FA8072',
        'tomato': '#FF6347',
        'orange': '#FFA500',
        'violet': '#EE82EE',
        'indigo': '#4B0082',
    }
    
    if color_str in color_names:
        return color_names[color_str]
    
    return color_str


def apply_style_to_text(text: str, style_config: Dict) -> str:
    """
    将样式配置应用到文本，生成带HTML标签的文本
    
    参数:
        text: 原始文本
        style_config: 样式配置字典（来自css_to_reportlab_style）
    
    返回:
        带HTML样式标签的文本
    """
    if not style_config:
        return text
    
    open_tags = []
    close_tags = []
    
    # 粗体
    if style_config.get('bold'):
        open_tags.append('<b>')
        close_tags.insert(0, '</b>')
    
    # 斜体
    if style_config.get('italic'):
        open_tags.append('<i>')
        close_tags.insert(0, '</i>')
    
    # 下划线
    if style_config.get('underline'):
        open_tags.append('<u>')
        close_tags.insert(0, '</u>')
    
    # 字体标签（颜色、背景色、字号）
    font_attrs = []
    if style_config.get('color'):
        font_attrs.append(f'color="{style_config["color"]}"')
    if style_config.get('bg_color'):
        font_attrs.append(f'backColor="{style_config["bg_color"]}"')
    if style_config.get('font_size'):
        font_attrs.append(f'size="{style_config["font_size"]}"')
    
    if font_attrs:
        open_tags.append(f'<font {" ".join(font_attrs)}>')
        close_tags.insert(0, '</font>')
    
    return ''.join(open_tags) + text + ''.join(close_tags)


def format_definition_list(
    words: List[str],
    definitions: Dict[str, str],
    word_color: str = "#631511",
    word_bg_color: str = None,
    word_bold: bool = False,
    word_underline: bool = False,
    defn_text_color: str = None,
    defn_font_size: int = 10,
    word_style_config: Dict = None,
    defn_style_config: Dict = None
) -> str:
    """
    格式化单词释义列表
    
    参数:
        words: 单词列表
        definitions: 释义字典
        word_color: 释义中单词的文字颜色（十六进制，如 #631511）
        word_bg_color: 释义中单词的背景颜色（可选，十六进制，如 #FFFF00）
        word_bold: 释义中单词是否加粗
        word_underline: 释义中单词是否下划线
        defn_text_color: 释义文字颜色（可选，默认与单词同色）
        defn_font_size: 释义字体大小（默认10）
        word_style_config: 单词完整样式配置（来自CSS，优先级高于单独参数）
        defn_style_config: 释义完整样式配置（来自CSS）
    
    返回:
        格式化后的HTML字符串（用于Paragraph渲染）
    """
    if not words:
        return ""
    
    # 释义颜色默认与单词同色
    if defn_text_color is None:
        defn_text_color = word_color
    
    items = []
    for word in words:
        defn = definitions.get(word, '')
        if defn:
            # 截取释义，避免过长
            if len(defn) > 30:
                defn = defn[:30] + '...'
            
            # 使用CSS样式配置（优先）或单独参数
            if word_style_config:
                word_formatted = apply_style_to_text(word, word_style_config)
            else:
                # 构建单词样式（传统方式）
                style_parts = []
                style_parts.append(f'color="{word_color}"')
                if word_bg_color:
                    style_parts.append(f'backColor="{word_bg_color}"')
                style_str = ' '.join(style_parts)
                
                open_tags = []
                close_tags = []
                
                if word_bold:
                    open_tags.append('<b>')
                    close_tags.insert(0, '</b>')
                if word_underline:
                    open_tags.append('<u>')
                    close_tags.insert(0, '</u>')
                
                open_tags.append(f'<font {style_str}>')
                close_tags.insert(0, '</font>')
                word_formatted = ''.join(open_tags) + word + ''.join(close_tags)
            
            # 释义样式
            if defn_style_config:
                defn_formatted = apply_style_to_text(defn, defn_style_config)
            else:
                defn_formatted = f'<font color="{defn_text_color}">{defn}</font>'
            
            items.append(f'{word_formatted} {defn_formatted}')
        else:
            # 无释义
            if word_style_config:
                word_formatted = apply_style_to_text(word, word_style_config)
            else:
                style_parts = []
                style_parts.append(f'color="{word_color}"')
                if word_bg_color:
                    style_parts.append(f'backColor="{word_bg_color}"')
                style_str = ' '.join(style_parts)
                
                open_tags = []
                close_tags = []
                
                if word_bold:
                    open_tags.append('<b>')
                    close_tags.insert(0, '</b>')
                if word_underline:
                    open_tags.append('<u>')
                    close_tags.insert(0, '</u>')
                
                open_tags.append(f'<font {style_str}>')
                close_tags.insert(0, '</font>')
                word_formatted = ''.join(open_tags) + word + ''.join(close_tags)
            
            items.append(word_formatted)
    
    return '；'.join(items)


def format_definition_for_canvas(
    words: List[str],
    definitions: Dict[str, str],
    text_color: tuple
) -> List[Tuple[str, bool]]:
    """
    格式化单词释义列表用于Canvas绘制
    
    参数:
        words: 单词列表
        definitions: 释义字典
        text_color: RGB颜色元组 (r, g, b)
    
    返回:
        列表，每个元素是 (文本, 是否高亮) 元组
    """
    if not words:
        return []
    
    items = []
    for word in words:
        defn = definitions.get(word, '')
        if defn:
            if len(defn) > 30:
                defn = defn[:30] + '...'
            items.append((word, True))  # 单词需要高亮
            items.append((f' {defn}；', False))  # 释义不高亮
        else:
            items.append((word, True))
            items.append(('；', False))
    
    return items


def _hex_to_rgb(hex_color: str) -> Tuple[float, float, float]:
    """
    将十六进制颜色转换为RGB元组（0-1范围）
    
    参数:
        hex_color: 十六进制颜色字符串，如 "#631511"
    
    返回:
        (r, g, b) 元组，每个值在0-1范围内
    """
    hex_color = hex_color.lstrip('#')
    r = int(hex_color[0:2], 16) / 255.0
    g = int(hex_color[2:4], 16) / 255.0
    b = int(hex_color[4:6], 16) / 255.0
    return (r, g, b)


def create_styles(font_name: str) -> dict:
    """创建文本样式"""
    styles = getSampleStyleSheet()
    
    title_style = ParagraphStyle(
        'TitleStyle',
        parent=styles['Heading1'],
        fontName=font_name,
        fontSize=24,
        alignment=1,
        spaceAfter=20,
        spaceBefore=10,
    )
    
    cell_style = ParagraphStyle(
        'CellStyle',
        parent=styles['Normal'],
        fontName=font_name,
        fontSize=11,
        leading=14,
        alignment=0,
        wordWrap='CJK',
    )
    
    header_style = ParagraphStyle(
        'HeaderStyle',
        parent=styles['Normal'],
        fontName=font_name,
        fontSize=12,
        leading=15,
        alignment=1,
    )
    
    return {
        'title': title_style,
        'cell': cell_style,
        'header': header_style,
    }


def add_page_number(canvas_obj, doc, font_name: str = "Helvetica", total_pages: int = 0):
    """
    添加页码到PDF右上角
    格式: X 页 / 总 X 页
    """
    page_num = canvas_obj.getPageNumber()
    
    # 如果总页数为0，显示当前页号；否则显示完整信息
    if total_pages > 0:
        text = f"{page_num} 页 / 总 {total_pages} 页"
    else:
        text = f"{page_num} 页"
    
    canvas_obj.saveState()
    canvas_obj.setFont(font_name, 10)
    
    # 计算右上角位置
    page_width = doc.pagesize[0]
    right_margin = 20 * mm
    top_margin = 15 * mm
    x = page_width - right_margin - canvas_obj.stringWidth(text, font_name, 10)
    y = doc.pagesize[1] - top_margin
    
    canvas_obj.drawString(x, y, text)
    canvas_obj.restoreState()


def generate_pdf(
    output_path: str,
    aligned_subs: List[Tuple[Optional[SubtitleEntry], Optional[SubtitleEntry]]],
    title: str = "双语台词本",
    font_path: Optional[str] = None,
    highlight_words: Optional[Set[str]] = None,
    definitions: Optional[Dict[str, str]] = None,
    highlight_text_color: str = "#631511",
    highlight_column: int = 2,
    lang1: str = None,
    lang2: str = None
):
    """
    生成PDF台词本
    
    高亮释义逻辑：
    1. 高亮单词用指定颜色标记
    2. 每页的高亮单词收集后，放在页面底部展示
    """
    font_name = "Helvetica"
    if font_path and Path(font_path).exists():
        try:
            font_name = "ChineseFont"
            register_chinese_font(font_path, font_name)
            print(f"使用指定字体: {font_path}")
        except Exception as e:
            print(f"警告：指定字体注册失败: {e}")
            font_name = _auto_detect_font()
    else:
        font_name = _auto_detect_font()
    
    page_size = get_page_size()
    
    doc = SimpleDocTemplate(
        output_path,
        pagesize=page_size,
        leftMargin=20*mm,
        rightMargin=20*mm,
        topMargin=15*mm,
        bottomMargin=5*mm,  # 释义现在是表格的一部分，减少下边距
    )
    
    styles = create_styles(font_name)
    
    # 创建释义样式
    base_styles = getSampleStyleSheet()
    defn_style = ParagraphStyle(
        'DefnStyle',
        parent=base_styles['Normal'],
        fontName=font_name,
        fontSize=10,
        leading=14,
        alignment=0,
        wordWrap='CJK',
    )
    
    story = []
    
    # 标题将在生成页面时添加，这里不再预先添加
    
    table_data = []
    
    # 检测语言并设置表格标题
    if lang1 is None or lang2 is None:
        # 自动检测语言
        all_text1 = " ".join([sub1.content for sub1, sub2 in aligned_subs if sub1])
        all_text2 = " ".join([sub2.content for sub1, sub2 in aligned_subs if sub2])
        if lang1 is None:
            lang1 = detect_language(all_text1)
        if lang2 is None:
            lang2 = detect_language(all_text2)
    
    lang1_name = get_language_name(lang1)
    lang2_name = get_language_name(lang2)
    
    # 创建时间轴样式（比正文小两个字号）
    timestamp_style = ParagraphStyle(
        'TimestampStyle',
        parent=styles['cell'],
        fontSize=9,  # 正文11，小两个字号
        textColor=colors.grey,
    )
    
    table_data.append([
        Paragraph("", styles['header']),  # 时间轴列标题为空
        Paragraph(lang1_name, styles['header']),
        Paragraph(lang2_name, styles['header']),
    ])
    
    # 收集所有高亮单词（按页分组）
    all_found_words = []  # 每个元素是该字幕行发现的单词
    seen_words = set()  # 全局已展示过释义的单词
    
    for sub1, sub2 in aligned_subs:
        text1 = sub1.content if sub1 else ""
        text2 = sub2.content if sub2 else ""
        
        # 时间轴（使用第一个字幕的开始时间）
        timestamp = ""
        if sub1:
            timestamp = format_timestamp(sub1.start_time)
        elif sub2:
            timestamp = format_timestamp(sub2.start_time)
        
        text1_raw = text1.replace('\n', '<br/>')
        text2_raw = text2.replace('\n', '<br/>')
        
        found_words_in_row = set()
        
        if highlight_words:
            if highlight_column in [1, 3] and text1:
                text1_raw, found1 = highlight_words_in_text(
                    text1_raw, highlight_words, highlight_text_color,
                    highlight_bg_color, highlight_bold, highlight_underline
                )
                found_words_in_row.update(found1)
            if highlight_column in [2, 3] and text2:
                text2_raw, found2 = highlight_words_in_text(
                    text2_raw, highlight_words, highlight_text_color,
                    highlight_bg_color, highlight_bold, highlight_underline
                )
                found_words_in_row.update(found2)
        
        # 创建时间轴单元格
        timestamp_cell = Paragraph(timestamp, timestamp_style) if timestamp else Paragraph("", timestamp_style)
        cell1 = Paragraph(text1_raw, styles['cell']) if text1_raw else Paragraph("", styles['cell'])
        cell2 = Paragraph(text2_raw, styles['cell']) if text2_raw else Paragraph("", styles['cell'])
        
        table_data.append([timestamp_cell, cell1, cell2])
        
        # 记录该行发现的单词
        new_words = [w for w in found_words_in_row if w not in seen_words]
        for w in new_words:
            seen_words.add(w)
        all_found_words.append(new_words)
    
    # 创建释义样式
    defn_style = ParagraphStyle(
        'DefnStyle',
        parent=styles['cell'],
        fontSize=9,
        textColor=colors.grey,
    )
    
    # 计算页面可用尺寸（单位：points）
    available_width = page_size[0] - 40*mm  # 页面宽度 - 左右边距
    timestamp_width = 15*mm  # 时间轴列宽度
    col_width = (available_width - timestamp_width) / 2  # 字幕列宽度
    total_defn_width = available_width  # 释义行总宽度
    
    # 页面可用高度（单位：points）
    available_height0 = page_size[1] - 10*mm - 5*mm - 35*mm  # A4高度 - 上边距 - 下边距 - 标题区域
    available_height = page_size[1] - 10*mm - 5*mm  # A4高度 - 上边距 - 下边距
    header_height = 8 * mm  # 表头高度
    row_padding = 1 * mm  # 每行的上下padding总和（紧凑布局）
    safety_margin = 3 * mm  # 安全边距
    
    # 动态计算每页内容
    pages_data = []
    
    # 当前页状态
    current_page_rows = []  # 当前页的行数据
    current_page_words = []  # 当前页收集的单词
    current_height = 0  # 当前页已使用高度（不含表头和释义）
    
    def calculate_row_height(row_data):
        """计算单行的实际高度（返回points单位）"""
        max_height = 0
        for idx, cell in enumerate(row_data):
            if isinstance(cell, Paragraph):
                if idx == 0:  # 时间轴列
                    w = timestamp_width
                elif idx == 1:  # 字幕1列
                    w = col_width
                else:  # 字幕2列
                    w = col_width
                # wrap返回(实际宽度, 实际高度)，单位都是points
                _, h = cell.wrap(w, 1000*mm)
                max_height = max(max_height, h)
        # 加上padding（已经是points单位）
        return max_height + row_padding
    
    def calculate_defn_height(words):
        """计算释义行的实际高度（返回points单位）"""
        if not words or not definitions:
            return 0
        defn_text = format_definition_list(
            words, definitions, 
            defn_word_color,  # 释义中单词颜色
            highlight_bg_color,  # 单词背景色（继承）
            highlight_bold,  # 单词加粗（继承）
            highlight_underline,  # 单词下划线（继承）
            defn_text_color,  # 释义文字颜色
            10,  # defn_font_size
            defn_word_style_config,  # CSS样式配置
            defn_text_style_config
        )
        if not defn_text:
            return 0
        defn_para = Paragraph(defn_text, defn_style)
        _, h = defn_para.wrap(total_defn_width, 1000*mm)
        # 加上padding（已经是points单位）
        return h + row_padding
    
    # 处理表头
    header_row = [
        Paragraph("", styles['header']),
        Paragraph(lang1_name, styles['header']),
        Paragraph(lang2_name, styles['header']),
    ]
    
    # 遍历所有内容行，动态分页
    for i, row in enumerate(table_data):
        if i == 0:
            # 跳过原始表头，使用新的表头
            continue
        
        # 计算该行高度
        row_height = calculate_row_height(row)
        
        # 计算添加该行后的释义高度
        test_words = current_page_words + list(all_found_words[i - 1] if i - 1 < len(all_found_words) else [])
        defn_height = calculate_defn_height(test_words)
        
        # 计算总需要高度：表头 + 当前已用 + 该行 + 释义 + 安全边距
        total_needed = header_height + current_height + row_height + defn_height + safety_margin
        
        if total_needed <= (available_height0 if len(pages_data) == 0 else available_height) or len(current_page_rows) == 0:
            # 可以添加到当前页，或者当前页为空（强制添加至少一行）
            current_page_rows.append(row)
            current_page_words = test_words
            current_height += row_height
        else:
            # 需要换页，先保存当前页
            pages_data.append((current_page_rows, current_page_words, current_height))
            # 开始新页面
            current_page_rows = [row]
            current_page_words = list(all_found_words[i - 1] if i - 1 < len(all_found_words) else [])
            current_height = row_height
    
    # 保存最后一页
    if current_page_rows:
        pages_data.append((current_page_rows, current_page_words, current_height))
    
    # 为每页创建表格并添加到story
    for page_idx, (page_rows, page_words, page_height) in enumerate(pages_data):
        if page_idx > 0:
            story.append(PageBreak())
        
        if page_idx == 0:
            story.append(Paragraph(title, styles['title']))
            story.append(Spacer(1, 10*mm))
        
        # 构建表格数据：表头 + 内容行 + 释义行
        page_table_data = [header_row]  # 添加表头
        page_table_data.extend(page_rows)  # 添加内容行
        
        # 添加释义行
        is_defn_row = False
        if page_words and definitions:
            defn_text = format_definition_list(
                page_words, definitions, highlight_text_color,
                highlight_bg_color, highlight_bold, highlight_underline,
                defn_text_color
            )
            if defn_text:
                defn_para = Paragraph(defn_text, defn_style)
                page_table_data.append([defn_para, "", ""])
                is_defn_row = True
        
        page_table = Table(page_table_data, colWidths=[timestamp_width, col_width, col_width])
        last_row_idx = len(page_table_data) - 1
        
        table_style = TableStyle([
            # 表头样式
            ('BACKGROUND', (0, 0), (-1, 0), colors.white),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
            ('FONTNAME', (0, 0), (-1, 0), font_name),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
            ('VALIGN', (0, 0), (-1, 0), 'MIDDLE'),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 2),
            ('TOPPADDING', (0, 0), (-1, 0), 2),
            
            # 内容区域样式
            ('BACKGROUND', (0, 1), (-1, -1), colors.white),
            ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
            ('FONTNAME', (0, 1), (-1, -1), font_name),
            ('FONTSIZE', (0, 1), (-1, -1), 11),
            ('ALIGN', (0, 1), (0, -1), 'LEFT'),
            ('ALIGN', (1, 1), (-1, -1), 'LEFT'),
            ('VALIGN', (0, 1), (-1, -1), 'TOP'),
            ('LEFTPADDING', (0, 0), (-1, -1), 4),
            ('RIGHTPADDING', (0, 0), (-1, -1), 4),
            ('BOTTOMPADDING', (0, 1), (-1, -1), 1),
            ('TOPPADDING', (0, 1), (-1, -1), 1),
            
            # 边框样式
            ('LINEBELOW', (0, 0), (-1, 0), 1, colors.black),
            ('LINEBELOW', (1, 1), (-1, -1), 0.5, colors.lightgrey),
        ])
        
        # 释义行特殊样式：合并整行（三列）
        if is_defn_row:
            # 解析背景颜色
            if defn_bg_color and defn_bg_color.startswith('#'):
                # 将十六进制颜色转换为 RGB
                r = int(defn_bg_color[1:3], 16) / 255.0
                g = int(defn_bg_color[3:5], 16) / 255.0
                b = int(defn_bg_color[5:7], 16) / 255.0
                bg_rgb = colors.Color(r, g, b)
            else:
                bg_rgb = colors.Color(0.96, 0.96, 0.96)  # 默认浅灰色
            
            table_style.add('BACKGROUND', (0, last_row_idx), (-1, last_row_idx), bg_rgb)
            table_style.add('SPAN', (0, last_row_idx), (-1, last_row_idx))  # 合并整行
            table_style.add('ALIGN', (0, last_row_idx), (-1, last_row_idx), 'LEFT')
            table_style.add('LINEBELOW', (0, last_row_idx), (-1, last_row_idx), 0, colors.white)
        
        page_table.setStyle(table_style)
        story.append(page_table)
    
    total_pages = len(pages_data)
    
    # 添加页码回调
    def add_page_number_callback(canvas_obj, doc_obj):
        page_num = canvas_obj.getPageNumber()
        text = f"{page_num} 页 / 总 {total_pages} 页"
        canvas_obj.saveState()
        canvas_obj.setFont(font_name, 10)
        page_width = doc_obj.pagesize[0]
        right_margin = 20 * mm
        top_margin = 15 * mm
        x = page_width - right_margin - canvas_obj.stringWidth(text, font_name, 10)
        y = doc_obj.pagesize[1] - top_margin
        canvas_obj.drawString(x, y, text)
        canvas_obj.restoreState()
    
    doc.build(story, onFirstPage=add_page_number_callback, onLaterPages=add_page_number_callback)
    
    print(f"PDF生成完成: {output_path}")
    print(f"页面大小: A4纸张 ({210}mm × {297}mm)")
    print(f"总页数: {total_pages}")
    if highlight_words:
        print(f"已高亮 {len(highlight_words)} 个单词")




def _auto_detect_font() -> str:
    """自动检测并注册中文字体，返回字体名称"""
    detected_font = find_chinese_font()
    
    if detected_font:
        try:
            font_name = "ChineseFont"
            register_chinese_font(detected_font, font_name)
            print(f"自动检测到中文字体: {detected_font}")
            return font_name
        except Exception as e:
            print(f"警告：自动检测的字体注册失败: {e}")
            print("警告：未找到可用的中文字体，中文可能显示为方框")
            print("请通过 --font 参数指定中文字体文件路径")
            return "Helvetica"
    else:
        print("警告：未在系统中检测到中文字体")
        print("请通过 --font 参数指定中文字体文件路径")
        print("推荐安装: 文泉驿微米黑 (wqy-microhei) 或 思源黑体 (Noto Sans CJK)")
        return "Helvetica"


def get_skill_dir() -> Path:
    """获取当前脚本所在的Skill目录"""
    return Path(__file__).resolve().parent.parent


def parse_parts_config(parts_args, config_path):
    """
    解析多部分字幕配置
    
    参数:
        parts_args: --parts 参数列表
        config_path: --config 配置文件路径
    
    返回:
        list: [{'subtitle1': '...', 'subtitle2': '...', 'title': '...'}, ...]
    """
    import json
    
    parts = []
    
    # 从配置文件读取
    if config_path:
        with open(config_path, 'r', encoding='utf-8') as f:
            config = json.load(f)
            if isinstance(config, list):
                parts.extend(config)
            elif isinstance(config, dict) and 'parts' in config:
                parts.extend(config['parts'])
    
    # 从命令行参数读取
    if parts_args:
        for part_str in parts_args:
            # 格式: 字幕1,字幕2,标题
            items = [x.strip() for x in part_str.split(',')]
            if len(items) >= 2:
                part = {
                    'subtitle1': items[0],
                    'subtitle2': items[1],
                    'title': items[2] if len(items) > 2 else f'Part {len(parts) + 1}'
                }
                parts.append(part)
    
    return parts


def generate_multi_part_pdf(
    output_path: str,
    parts_config: List[Dict],
    main_title: str,
    font_path: Optional[str],
    highlight_words: Optional[Set[str]],
    definitions: Optional[Dict[str, str]],
    highlight_column: int,
    highlight_styles: Optional[Dict] = None,
    defn_styles: Optional[Dict] = None
):
    """
    生成多部分PDF台词本
    
    参数:
        output_path: 输出PDF路径
        parts_config: 多部分配置列表
        main_title: 总标题
        font_path: 字体路径
        highlight_words: 高亮词汇集合
        definitions: 释义字典
        highlight_column: 高亮列
        highlight_styles: 高亮样式配置
            - 基础参数: {'text_color', 'bg_color', 'bold', 'underline'}
            - CSS样式: {'style_config': {...}}
        defn_styles: 释义样式配置
            - 基础参数: {'word_color', 'text_color', 'bg_color'}
            - CSS样式: {'word_style_config': {...}, 'text_style_config': {...}}
    """
    # 解析高亮样式
    if highlight_styles is None:
        highlight_styles = {}
    highlight_text_color = highlight_styles.get('text_color', '#631511')
    highlight_bg_color = highlight_styles.get('bg_color', None)
    highlight_bold = highlight_styles.get('bold', False)
    highlight_underline = highlight_styles.get('underline', False)
    highlight_style_config = highlight_styles.get('style_config', None)  # CSS样式配置
    
    # 解析释义样式
    if defn_styles is None:
        defn_styles = {}
    # 释义中单词颜色，默认与高亮颜色相同
    defn_word_color = defn_styles.get('word_color', highlight_text_color)
    # 释义文字颜色，默认与单词颜色相同
    defn_text_color = defn_styles.get('text_color', defn_word_color)
    defn_bg_color = defn_styles.get('bg_color', '#F5F5F5')
    # CSS样式配置
    defn_word_style_config = defn_styles.get('word_style_config', None)
    defn_text_style_config = defn_styles.get('text_style_config', None)
    
    font_name = "Helvetica"
    if font_path and Path(font_path).exists():
        try:
            font_name = "ChineseFont"
            register_chinese_font(font_path, font_name)
            print(f"使用指定字体: {font_path}")
        except Exception as e:
            print(f"警告：指定字体注册失败: {e}")
            font_name = _auto_detect_font()
    else:
        font_name = _auto_detect_font()
    
    page_size = get_page_size()
    
    # 创建文档（使用SimpleDocTemplate更简单）
    doc = SimpleDocTemplate(
        output_path,
        pagesize=page_size,
        leftMargin=20*mm,
        rightMargin=20*mm,
        topMargin=15*mm,
        bottomMargin=5*mm,
    )
    
    styles = create_styles(font_name)
    
    # 创建释义样式
    base_styles = getSampleStyleSheet()
    defn_style = ParagraphStyle(
        'DefnStyle',
        parent=base_styles['Normal'],
        fontName=font_name,
        fontSize=10,
        leading=14,
        alignment=0,
        wordWrap='CJK',
    )
    
    all_story = []
    total_pages = 0
    
    # 处理每个部分
    for part_idx, part in enumerate(parts_config):
        print(f"\n处理第 {part_idx + 1} 部分: {part.get('title', f'Part {part_idx + 1}')}")
        
        # 解析字幕
        print(f"  解析字幕文件1: {part['subtitle1']}")
        subs1 = parse_subtitle(part['subtitle1'])
        print(f"    共 {len(subs1)} 条字幕")
        
        print(f"  解析字幕文件2: {part['subtitle2']}")
        subs2 = parse_subtitle(part['subtitle2'])
        print(f"    共 {len(subs2)} 条字幕")
        
        print("  对齐字幕...")
        aligned = align_subtitles(subs1, subs2)
        print(f"    共 {len(aligned)} 对字幕")
        
        # 生成该部分的story
        part_story, part_pages = generate_part_story(
            aligned,
            part.get('title', f'Part {part_idx + 1}'),
            font_name,
            styles,
            defn_style,
            page_size,
            highlight_words,
            definitions,
            highlight_text_color,
            highlight_column,
            highlight_bg_color,
            highlight_bold,
            highlight_underline,
            defn_word_color,
            defn_text_color,
            defn_bg_color,
            highlight_style_config,
            defn_word_style_config,
            defn_text_style_config
        )
        
        # 如果不是第一部分，先添加分页
        if part_idx > 0:
            all_story.append(PageBreak())
        
        all_story.extend(part_story)
        total_pages += part_pages
        print(f"  该部分页数: {part_pages}")
    
    # 添加页码回调
    def add_page_number_callback(canvas_obj, doc_obj):
        page_num = canvas_obj.getPageNumber()
        text = f"{page_num} 页 / 总 {total_pages} 页"
        canvas_obj.saveState()
        canvas_obj.setFont(font_name, 10)
        page_width = doc_obj.pagesize[0]
        right_margin = 20 * mm
        top_margin = 15 * mm
        x = page_width - right_margin - canvas_obj.stringWidth(text, font_name, 10)
        y = doc_obj.pagesize[1] - top_margin
        canvas_obj.drawString(x, y, text)
        canvas_obj.restoreState()
    
    # 构建PDF
    print(f"\n构建PDF: {output_path}")
    print(f"总页数: {total_pages}")
    doc.build(all_story, onFirstPage=add_page_number_callback, onLaterPages=add_page_number_callback)
    
    # 统计页数
    output_file = Path(output_path)
    if output_file.exists():
        size_kb = output_file.stat().st_size / 1024
        print(f"PDF生成完成: {output_path}")
        print(f"文件大小: {size_kb:.2f} KB")


def generate_part_story(
    aligned_subs: List[Tuple[Optional[SubtitleEntry], Optional[SubtitleEntry]]],
    title: str,
    font_name: str,
    styles: Dict,
    defn_style: ParagraphStyle,
    page_size: Tuple[float, float],
    highlight_words: Optional[Set[str]] = None,
    definitions: Optional[Dict[str, str]] = None,
    highlight_text_color: str = "#631511",
    highlight_column: int = 2,
    highlight_bg_color: str = None,
    highlight_bold: bool = False,
    highlight_underline: bool = False,
    defn_word_color: str = None,
    defn_text_color: str = None,
    defn_bg_color: str = '#F5F5F5',
    highlight_style_config: Dict = None,
    defn_word_style_config: Dict = None,
    defn_text_style_config: Dict = None,
    lang1: str = None,
    lang2: str = None
) -> List:
    """
    生成单个部分的story（不直接生成PDF）
    
    参数:
        defn_word_color: 释义中单词颜色（默认与 highlight_text_color 相同）
        defn_text_color: 释义文字颜色（默认与 defn_word_color 相同）
        highlight_style_config: 高亮单词的CSS样式配置（优先级高于单独参数）
        defn_word_style_config: 释义中单词的CSS样式配置
        defn_text_style_config: 释义文字的CSS样式配置
    
    返回:
        List: story对象列表
    """
    # 默认值处理
    if defn_word_color is None:
        defn_word_color = highlight_text_color
    if defn_text_color is None:
        defn_text_color = defn_word_color
    
    story = []
    
    # 添加标题
    story.append(Paragraph(title, styles['title']))
    story.append(Spacer(1, 10*mm))
    
    table_data = []
    
    # 检测语言并设置表格标题
    if not lang1 or not lang2:
        # 自动检测语言
        sample_text1 = ""
        sample_text2 = ""
        count = 0
        for sub1, sub2 in aligned_subs:
            if sub1 and not sample_text1:
                sample_text1 = sub1.content
            if sub2 and not sample_text2:
                sample_text2 = sub2.content
            if sample_text1 and sample_text2:
                break
            count += 1
            if count > 10:
                break
        
        lang1 = detect_language(sample_text1) if sample_text1 else 'zh'
        lang2 = detect_language(sample_text2) if sample_text2 else 'en'
    
    lang1_name = LANGUAGE_NAMES.get(lang1, lang1)
    lang2_name = LANGUAGE_NAMES.get(lang2, lang2)
    
    # 添加表头
    header_row = [
        Paragraph("", styles['header']),
        Paragraph(lang1_name, styles['header']),
        Paragraph(lang2_name, styles['header']),
    ]
    table_data.append(header_row)
    
    # 收集所有高亮单词（用于去重）
    seen_words = set()
    all_found_words = []  # 每行发现的单词列表
    
    # 处理每对字幕
    for sub1, sub2 in aligned_subs:
        text1 = sub1.content if sub1 else ""
        text2 = sub2.content if sub2 else ""
        
        # 时间轴（使用第一个字幕的开始时间）
        timestamp = ""
        if sub1:
            timestamp = format_timestamp(sub1.start_time)
        elif sub2:
            timestamp = format_timestamp(sub2.start_time)
        
        text1_raw = text1.replace('\n', '<br/>')
        text2_raw = text2.replace('\n', '<br/>')
        
        found_words_in_row = set()
        
        if highlight_words:
            if highlight_column in [1, 3] and text1:
                text1_raw, found1 = highlight_words_in_text(
                    text1_raw, highlight_words, highlight_text_color,
                    highlight_bg_color, highlight_bold, highlight_underline,
                    highlight_style_config
                )
                found_words_in_row.update(found1)
            if highlight_column in [2, 3] and text2:
                text2_raw, found2 = highlight_words_in_text(
                    text2_raw, highlight_words, highlight_text_color,
                    highlight_bg_color, highlight_bold, highlight_underline,
                    highlight_style_config
                )
                found_words_in_row.update(found2)
        
        # 创建时间轴单元格
        timestamp_cell = Paragraph(timestamp, styles['cell']) if timestamp else Paragraph("", styles['cell'])
        cell1 = Paragraph(text1_raw, styles['cell']) if text1_raw else Paragraph("", styles['cell'])
        cell2 = Paragraph(text2_raw, styles['cell']) if text2_raw else Paragraph("", styles['cell'])
        
        table_data.append([timestamp_cell, cell1, cell2])
        
        # 记录该行发现的单词
        new_words = [w for w in found_words_in_row if w not in seen_words]
        for w in new_words:
            seen_words.add(w)
        all_found_words.append(new_words)
    
    # 计算页面可用尺寸（单位：points）
    available_width = page_size[0] - 40*mm  # 页面宽度 - 左右边距
    timestamp_width = 15*mm  # 时间轴列宽度
    col_width = (available_width - timestamp_width) / 2  # 字幕列宽度
    total_defn_width = available_width  # 释义行总宽度
    
    # 页面可用高度（单位：points）
    # 第一页有标题，需要扣除标题区域；后续页面无需扣除
    available_height0 = page_size[1] - 10*mm - 5*mm - 35*mm  # 第一页：A4高度 - 上边距 - 下边距 - 标题区域
    available_height = page_size[1] - 10*mm - 5*mm  # 后续页面：A4高度 - 上边距 - 下边距
    header_height = 8 * mm  # 表头高度
    row_padding = 1 * mm  # 每行的上下padding总和（紧凑布局）
    safety_margin = 3 * mm  # 安全边距
    
    # 动态计算每页内容
    pages_data = []
    
    # 当前页状态
    current_page_rows = []  # 当前页的行数据
    current_page_words = []  # 当前页收集的单词
    current_height = 0  # 当前页已使用高度（不含表头和释义）
    
    def calculate_row_height(row_data):
        """计算单行的实际高度（返回points单位）"""
        max_height = 0
        for idx, cell in enumerate(row_data):
            if isinstance(cell, Paragraph):
                if idx == 0:  # 时间轴列
                    w = timestamp_width
                elif idx == 1:  # 字幕1列
                    w = col_width
                else:  # 字幕2列
                    w = col_width
                # wrap返回(实际宽度, 实际高度)，单位都是points
                _, h = cell.wrap(w, 1000*mm)
                max_height = max(max_height, h)
        # 加上padding（已经是points单位）
        return max_height + row_padding
    
    def calculate_defn_height(words):
        """计算释义行的实际高度（返回points单位）"""
        if not words or not definitions:
            return 0
        defn_text = format_definition_list(
            words, definitions, 
            defn_word_color,  # 释义中单词颜色
            highlight_bg_color,  # 单词背景色（继承）
            highlight_bold,  # 单词加粗（继承）
            highlight_underline,  # 单词下划线（继承）
            defn_text_color  # 释义文字颜色
        )
        if not defn_text:
            return 0
        defn_para = Paragraph(defn_text, defn_style)
        _, h = defn_para.wrap(total_defn_width, 1000*mm)
        # 加上padding（已经是points单位）
        return h + row_padding
    
    # 处理表头
    header_row = [
        Paragraph("", styles['header']),
        Paragraph(lang1_name, styles['header']),
        Paragraph(lang2_name, styles['header']),
    ]
    
    # 遍历所有内容行，动态分页
    for i, row in enumerate(table_data):
        if i == 0:
            # 跳过原始表头，使用新的表头
            continue
        
        # 计算该行高度
        row_height = calculate_row_height(row)
        
        # 计算添加该行后的释义高度
        test_words = current_page_words + list(all_found_words[i - 1] if i - 1 < len(all_found_words) else [])
        defn_height = calculate_defn_height(test_words)
        
        # 计算总需要高度：表头 + 当前已用 + 该行 + 释义 + 安全边距
        total_needed = header_height + current_height + row_height + defn_height + safety_margin
        
        # 根据当前页数选择可用高度（第一页需考虑标题区域）
        current_available_height = available_height0 if len(pages_data) == 0 else available_height
        
        if total_needed <= current_available_height or len(current_page_rows) == 0:
            # 可以添加到当前页，或者当前页为空（强制添加至少一行）
            current_page_rows.append(row)
            current_page_words = test_words
            current_height += row_height
        else:
            # 需要换页，先保存当前页
            pages_data.append((current_page_rows, current_page_words, current_height))
            # 开始新页面
            current_page_rows = [row]
            current_page_words = list(all_found_words[i - 1] if i - 1 < len(all_found_words) else [])
            current_height = row_height
    
    # 保存最后一页
    if current_page_rows:
        pages_data.append((current_page_rows, current_page_words, current_height))
    
    # 为每页创建表格并添加到story
    for page_idx, (page_rows, page_words, page_height) in enumerate(pages_data):
        if page_idx > 0:
            story.append(PageBreak())
        
        # 构建表格数据：表头 + 内容行 + 释义行
        page_table_data = [header_row]  # 添加表头
        page_table_data.extend(page_rows)  # 添加内容行
        
        # 添加释义行
        is_defn_row = False
        if page_words and definitions:
            defn_text = format_definition_list(
                page_words, definitions,
                defn_word_color,  # 释义中单词颜色
                highlight_bg_color,  # 单词背景色（继承）
                highlight_bold,  # 单词加粗（继承）
                highlight_underline,  # 单词下划线（继承）
                defn_text_color,  # 释义文字颜色
                10,  # defn_font_size
                defn_word_style_config,  # CSS样式配置
                defn_text_style_config
            )
            if defn_text:
                defn_para = Paragraph(defn_text, defn_style)
                page_table_data.append([defn_para, "", ""])
                is_defn_row = True
        
        page_table = Table(page_table_data, colWidths=[timestamp_width, col_width, col_width])
        last_row_idx = len(page_table_data) - 1
        
        table_style = TableStyle([
            # 表头样式
            ('BACKGROUND', (0, 0), (-1, 0), colors.white),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
            ('FONTNAME', (0, 0), (-1, 0), font_name),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
            ('VALIGN', (0, 0), (-1, 0), 'MIDDLE'),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 2),
            ('TOPPADDING', (0, 0), (-1, 0), 2),
            
            # 内容区域样式
            ('BACKGROUND', (0, 1), (-1, -1), colors.white),
            ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
            ('FONTNAME', (0, 1), (-1, -1), font_name),
            ('FONTSIZE', (0, 1), (-1, -1), 11),
            ('ALIGN', (0, 1), (0, -1), 'LEFT'),
            ('ALIGN', (1, 1), (-1, -1), 'LEFT'),
            ('VALIGN', (0, 1), (-1, -1), 'TOP'),
            ('LEFTPADDING', (0, 0), (-1, -1), 4),
            ('RIGHTPADDING', (0, 0), (-1, -1), 4),
            ('BOTTOMPADDING', (0, 1), (-1, -1), 1),
            ('TOPPADDING', (0, 1), (-1, -1), 1),
            
            # 边框样式
            ('LINEBELOW', (0, 0), (-1, 0), 1, colors.black),
            ('LINEBELOW', (1, 1), (-1, -1), 0.5, colors.lightgrey),
        ])
        
        # 释义行特殊样式：合并整行（三列）
        if is_defn_row:
            table_style.add('BACKGROUND', (0, last_row_idx), (-1, last_row_idx), 
                          colors.Color(0.95, 0.95, 0.95))
            table_style.add('SPAN', (0, last_row_idx), (-1, last_row_idx))  # 合并整行
            table_style.add('ALIGN', (0, last_row_idx), (-1, last_row_idx), 'LEFT')
            table_style.add('LINEBELOW', (0, last_row_idx), (-1, last_row_idx), 0, colors.white)
        
        page_table.setStyle(table_style)
        story.append(page_table)
    
    # 返回 story 和页数
    return story, len(pages_data)


def main():
    parser = argparse.ArgumentParser(description='双语字幕转PDF台词本')
    
    # 多部分支持
    parser.add_argument('--parts', '-p', action='append', 
                        help='多对字幕（可多次使用），格式：字幕1,字幕2,标题')
    parser.add_argument('--config', '-c', 
                        help='JSON配置文件路径，指定多对字幕')
    
    # 单对字幕模式（向后兼容）
    parser.add_argument('--subtitle1', '-s1', help='字幕文件1路径（左列）')
    parser.add_argument('--subtitle2', '-s2', help='字幕文件2路径（右列）')
    parser.add_argument('--single-file', '-sf', help='单文件双语模式')
    
    parser.add_argument('--output', '-o', required=True, help='输出PDF文件路径')
    parser.add_argument('--title', '-t', default='双语台词本', help='台词本标题（单对字幕模式）')
    parser.add_argument('--font', '-f', help='自定义字体路径（支持中文）')
    
    # 单词高亮参数 - 按难度等级
    parser.add_argument('--highlight-cet4', action='store_true', 
                        help='高亮四级及以上词汇')
    parser.add_argument('--highlight-cet6', action='store_true', 
                        help='高亮六级及以上词汇')
    parser.add_argument('--highlight-tem4', action='store_true', 
                        help='高亮专四及以上词汇')
    parser.add_argument('--highlight-tem8', action='store_true', 
                        help='高亮专八及以上词汇')
    parser.add_argument('--highlight-kaoyan', action='store_true', 
                        help='高亮考研及以上词汇')
    parser.add_argument('--highlight-ielts', action='store_true', 
                        help='高亮雅思及以上词汇')
    parser.add_argument('--highlight-toefl', action='store_true', 
                        help='高亮托福及以上词汇')
    parser.add_argument('--highlight-gmat', action='store_true', 
                        help='高亮GMAT及以上词汇')
    parser.add_argument('--highlight-gre', action='store_true', 
                        help='高亮GRE及以上词汇')
    parser.add_argument('--highlight-sat', action='store_true', 
                        help='高亮SAT词汇')
    
    # 单词高亮参数 - 按分类
    parser.add_argument('--highlight-hot', action='store_true', 
                        help='高亮热门单词（四级、六级、考研）')
    parser.add_argument('--highlight-college', action='store_true', 
                        help='高亮大学单词（四级、六级、考研、专四、专八）')
    parser.add_argument('--highlight-abroad', action='store_true', 
                        help='高亮出国单词（雅思、托福、GMAT、GRE、SAT）')
    
    parser.add_argument('--highlight-words', '-hw', 
                        help='自定义高亮词汇（文件路径或逗号分隔的词汇）')
    
    # CSS样式文件（优先级最高）
    parser.add_argument('--style-css', '-sc', 
                        help='CSS样式文件路径，支持复杂样式定义')
    
    # 内联CSS样式字符串
    parser.add_argument('--highlight-style', '-hs', 
                        help='台词中高亮单词的CSS样式（如 "color: red; background: yellow; font-weight: bold"）')
    parser.add_argument('--defn-word-style', '-dws',
                        help='释义中单词的CSS样式')
    parser.add_argument('--defn-text-style', '-dts',
                        help='释义文字的CSS样式')
    
    # 高亮样式参数（简单模式，CSS优先级更高）
    parser.add_argument('--highlight-color', '-hc', default='#631511',
                        help='高亮文字颜色（默认: #631511 深红色）')
    parser.add_argument('--highlight-bg-color', '-hbc', default=None,
                        help='高亮背景颜色（可选，如 #FFFF00 黄色）')
    parser.add_argument('--highlight-bold', '-hb', action='store_true',
                        help='高亮单词加粗')
    parser.add_argument('--highlight-underline', '-hu', action='store_true',
                        help='高亮单词下划线')
    parser.add_argument('--highlight-column', '-hcol', type=int, default=2, choices=[1, 2, 3],
                        help='高亮列: 1=左列, 2=右列, 3=两列都高亮（默认: 2）')
    
    # 释义样式参数
    parser.add_argument('--defn-word-color', '-dwc', default=None,
                        help='释义中单词颜色（默认与高亮颜色相同）')
    parser.add_argument('--defn-color', '-dc', default=None,
                        help='释义文字颜色（默认与释义单词同色）')
    parser.add_argument('--defn-bg-color', '-dbc', default='#F5F5F5',
                        help='释义行背景颜色（默认: #F5F5F5 浅灰色）')
    
    args = parser.parse_args()
    
    # 解析多部分配置
    parts_config = parse_parts_config(args.parts, args.config)
    
    # 判断模式：多部分模式 or 单对字幕模式
    multi_part_mode = len(parts_config) > 0
    
    if not multi_part_mode:
        # 单对字幕模式（向后兼容）
        if args.single_file:
            print("单文件模式暂不支持，请提供两个字幕文件")
            sys.exit(1)
        else:
            if not args.subtitle1 or not args.subtitle2:
                print("错误：请提供两个字幕文件路径（--subtitle1 和 --subtitle2）")
                print("或者使用 --parts 或 --config 指定多对字幕")
                sys.exit(1)
            
            # 转换为多部分配置格式
            parts_config = [{
                'subtitle1': args.subtitle1,
                'subtitle2': args.subtitle2,
                'title': args.title
            }]
    
    # 加载高亮词汇
    highlight_words = set()
    definitions = {}
    skill_dir = get_skill_dir()
    vocab_dict = None
    
    # 确定最低难度等级
    min_level = 0
    
    if args.highlight_cet4:
        min_level = max(min_level, WORD_LEVELS['cet4'])
    if args.highlight_cet6:
        min_level = max(min_level, WORD_LEVELS['cet6'])
    if args.highlight_tem4:
        min_level = max(min_level, WORD_LEVELS['tem4'])
    if args.highlight_tem8:
        min_level = max(min_level, WORD_LEVELS['tem8'])
    if args.highlight_kaoyan:
        min_level = max(min_level, WORD_LEVELS['kaoyan'])
    if args.highlight_ielts:
        min_level = max(min_level, WORD_LEVELS['ielts'])
    if args.highlight_toefl:
        min_level = max(min_level, WORD_LEVELS['toefl'])
    if args.highlight_gmat:
        min_level = max(min_level, WORD_LEVELS['gmat'])
    if args.highlight_gre:
        min_level = max(min_level, WORD_LEVELS['gre'])
    if args.highlight_sat:
        min_level = max(min_level, WORD_LEVELS['sat'])
    
    # 按难度等级高亮
    if min_level > 0:
        vocab_dict, definitions = load_all_vocab_files(skill_dir)
        highlight_words = get_highlight_words_by_level(min_level, vocab_dict)
        
        # 显示高亮范围
        level_names = {
            1: "四级",
            2: "六级/专四",
            3: "专八/考研",
            4: "雅思/托福",
            5: "GMAT/GRE/SAT"
        }
        print(f"高亮等级: {level_names.get(min_level, '未知')} 及以上")
    
    # 按分类高亮
    if args.highlight_hot or args.highlight_college or args.highlight_abroad:
        if vocab_dict is None:
            vocab_dict, definitions = load_all_vocab_files(skill_dir)
        
        if args.highlight_hot:
            words = get_highlight_words_by_category('hot', vocab_dict)
            highlight_words.update(words)
            print(f"高亮分类: 热门单词 ({len(words)} 个)")
        
        if args.highlight_college:
            words = get_highlight_words_by_category('college', vocab_dict)
            highlight_words.update(words)
            print(f"高亮分类: 大学单词 ({len(words)} 个)")
        
        if args.highlight_abroad:
            words = get_highlight_words_by_category('abroad', vocab_dict)
            highlight_words.update(words)
            print(f"高亮分类: 出国单词 ({len(words)} 个)")
    
    if args.highlight_words:
        custom_words = load_custom_words(args.highlight_words)
        highlight_words.update(custom_words)
    
    # 解析CSS样式（优先级最高）
    css_styles = {}
    if args.style_css:
        css_styles = parse_css_file(args.style_css)
        if css_styles:
            print(f"已加载CSS样式文件: {args.style_css}")
    
    # 解析内联CSS样式
    inline_highlight_style = None
    inline_defn_word_style = None
    inline_defn_text_style = None
    
    if args.highlight_style:
        inline_highlight_style = css_to_reportlab_style(parse_css_style(args.highlight_style))
    if args.defn_word_style:
        inline_defn_word_style = css_to_reportlab_style(parse_css_style(args.defn_word_style))
    if args.defn_text_style:
        inline_defn_text_style = css_to_reportlab_style(parse_css_style(args.defn_text_style))
    
    # 收集高亮样式参数（CSS优先）
    highlight_styles = {
        'text_color': args.highlight_color,
        'bg_color': args.highlight_bg_color,
        'bold': args.highlight_bold,
        'underline': args.highlight_underline,
    }
    
    # 应用CSS样式到高亮样式
    if 'highlight-word' in css_styles:
        css_config = css_to_reportlab_style(css_styles['highlight-word'])
        highlight_styles['style_config'] = css_config
        print(f"  应用CSS样式: highlight-word")
    elif inline_highlight_style:
        highlight_styles['style_config'] = inline_highlight_style
        print(f"  应用内联样式: highlight")
    
    # 收集释义样式参数
    # defn_word_color 默认使用 highlight_color
    defn_word_color = args.defn_word_color if args.defn_word_color else args.highlight_color
    # defn_text_color 默认使用 defn_word_color
    defn_text_color = args.defn_color if args.defn_color else defn_word_color
    
    defn_styles = {
        'word_color': defn_word_color,
        'text_color': defn_text_color,
        'bg_color': args.defn_bg_color,
    }
    
    # 应用CSS样式到释义样式
    if 'definition-word' in css_styles:
        defn_styles['word_style_config'] = css_to_reportlab_style(css_styles['definition-word'])
        print(f"  应用CSS样式: definition-word")
    elif inline_defn_word_style:
        defn_styles['word_style_config'] = inline_defn_word_style
    
    if 'definition-text' in css_styles:
        defn_styles['text_style_config'] = css_to_reportlab_style(css_styles['definition-text'])
        print(f"  应用CSS样式: definition-text")
    elif inline_defn_text_style:
        defn_styles['text_style_config'] = inline_defn_text_style
    
    # 生成PDF
    generate_multi_part_pdf(
        args.output,
        parts_config,
        args.title if not multi_part_mode else "双语台词本",
        args.font,
        highlight_words if highlight_words else None,
        definitions if highlight_words else None,
        args.highlight_column,
        highlight_styles,
        defn_styles
    )
    
    output_path = Path(args.output)
    if output_path.exists():
        size_kb = output_path.stat().st_size / 1024
        print(f"页面大小: A4纸张 (210mm × 297mm)")
        print(f"文件大小: {size_kb:.2f} KB")


if __name__ == '__main__':
    main()
