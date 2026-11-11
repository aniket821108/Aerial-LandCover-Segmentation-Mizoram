import os
import sys
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import qn, nsdecls

def set_cell_background(cell, hex_color):
    """Sets cell shading."""
    tcPr = cell._element.get_or_add_tcPr()
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{hex_color}"/>')
    tcPr.append(shd)

def set_cell_margins(cell, top=120, bottom=120, left=160, right=160):
    """Sets cell padding in dxa (1 pt = 20 dxa)."""
    tcPr = cell._element.get_or_add_tcPr()
    tcMar = parse_xml(
        f'<w:tcMar {nsdecls("w")}>'
        f'<w:top w:w="{top}" w:type="dxa"/>'
        f'<w:bottom w:w="{bottom}" w:type="dxa"/>'
        f'<w:left w:w="{left}" w:type="dxa"/>'
        f'<w:right w:w="{right}" w:type="dxa"/>'
        f'</w:tcMar>'
    )
    tcPr.append(tcMar)

def create_report():
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    results_dir = os.path.join(base_dir, "results")
    output_docx = os.path.join(base_dir, "docs", "FINAL_ACADEMIC_PROJECT_REPORT.docx")

    doc = Document()

    # Page Margins (1 inch all around, left 1.25 inch for binding)
    sections = doc.sections
    for section in sections:
        section.top_margin = Inches(1.0)
        section.bottom_margin = Inches(1.0)
        section.left_margin = Inches(1.25)
        section.right_margin = Inches(1.0)

    # Styles
    style_normal = doc.styles['Normal']
    font = style_normal.font
    font.name = 'Times New Roman'
    font.size = Pt(12)
    font.color.rgb = RGBColor(30, 41, 59) # Slate 800
    style_normal.paragraph_format.line_spacing = 1.35
    style_normal.paragraph_format.space_after = Pt(6)

    def add_p(text, bold=False, italic=False, align=WD_ALIGN_PARAGRAPH.LEFT, space_before=0, space_after=6, font_size=12, color=RGBColor(30, 41, 59)):
        p = doc.add_paragraph()
        p.alignment = align
        p.paragraph_format.space_before = Pt(space_before)
        p.paragraph_format.space_after = Pt(space_after)
        p.paragraph_format.line_spacing = 1.35
        run = p.add_run(text)
        run.bold = bold
        run.italic = italic
        run.font.name = 'Times New Roman'
        run.font.size = Pt(font_size)
        run.font.color.rgb = color
        return p

    def add_h1(text):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(18)
        p.paragraph_format.space_after = Pt(8)
        p.paragraph_format.keep_with_next = True
        run = p.add_run(text)
        run.bold = True
        run.font.name = 'Times New Roman'
        run.font.size = Pt(16)
        run.font.color.rgb = RGBColor(15, 23, 42) # Slate 900
        return p

    def add_h2(text):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(12)
        p.paragraph_format.space_after = Pt(4)
        p.paragraph_format.keep_with_next = True
        run = p.add_run(text)
        run.bold = True
        run.font.name = 'Times New Roman'
        run.font.size = Pt(13)
        run.font.color.rgb = RGBColor(30, 58, 138) # Deep Blue
        return p

    def add_h3(text):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(8)
        p.paragraph_format.space_after = Pt(2)
        p.paragraph_format.keep_with_next = True
        run = p.add_run(text)
        run.bold = True
        run.italic = True
        run.font.name = 'Times New Roman'
        run.font.size = Pt(12)
        run.font.color.rgb = RGBColor(51, 65, 85)
        return p

    def add_callout(text, prefix="KEY FINDING:"):
        table = doc.add_table(rows=1, cols=1)
        table.alignment = WD_TABLE_ALIGNMENT.CENTER
        cell = table.cell(0, 0)
        set_cell_background(cell, "F1F5F9") # light slate
        set_cell_margins(cell, top=140, bottom=140, left=200, right=200)
        p = cell.paragraphs[0]
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after = Pt(0)
        p.paragraph_format.line_spacing = 1.25
        run_b = p.add_run(f"{prefix} ")
        run_b.bold = True
        run_b.font.name = 'Times New Roman'
        run_b.font.size = Pt(10.5)
        run_b.font.color.rgb = RGBColor(2, 132, 199)
        run_t = p.add_run(text)
        run_t.font.name = 'Times New Roman'
        run_t.font.size = Pt(10.5)
        run_t.font.color.rgb = RGBColor(30, 41, 59)
        doc.add_paragraph().paragraph_format.space_after = Pt(4)

    def add_fig(img_name, caption_text, width=Inches(5.5)):
        img_path = os.path.join(results_dir, img_name)
        if os.path.exists(img_path):
            p = doc.add_paragraph()
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p.paragraph_format.space_before = Pt(10)
            p.paragraph_format.space_after = Pt(4)
            p.paragraph_format.keep_with_next = True
            run = p.add_run()
            run.add_picture(img_path, width=width)
            
            cp = doc.add_paragraph()
            cp.alignment = WD_ALIGN_PARAGRAPH.CENTER
            cp.paragraph_format.space_before = Pt(2)
            cp.paragraph_format.space_after = Pt(12)
            c_run = cp.add_run(caption_text)
            c_run.font.name = 'Times New Roman'
            c_run.font.size = Pt(10)
            c_run.italic = True
            c_run.font.color.rgb = RGBColor(71, 85, 105)

    def add_styled_table(headers, rows_data, col_widths=None):
        table = doc.add_table(rows=len(rows_data) + 1, cols=len(headers))
        table.alignment = WD_TABLE_ALIGNMENT.CENTER
        
        # Header Row
        hdr_cells = table.rows[0].cells
        for i, header_text in enumerate(headers):
            hdr_cells[i].text = header_text
            set_cell_background(hdr_cells[i], "1E293B") # Dark slate
            set_cell_margins(hdr_cells[i], top=140, bottom=140, left=140, right=140)
            p = hdr_cells[i].paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p.runs[0].font.name = 'Times New Roman'
            p.runs[0].font.bold = True
            p.runs[0].font.size = Pt(10.5)
            p.runs[0].font.color.rgb = RGBColor(255, 255, 255)
            
        # Data Rows
        for r_idx, row in enumerate(rows_data):
            row_cells = table.rows[r_idx + 1].cells
            bg_color = "F8FAFC" if r_idx % 2 == 1 else "FFFFFF"
            for c_idx, val in enumerate(row):
                row_cells[c_idx].text = str(val)
                set_cell_background(row_cells[c_idx], bg_color)
                set_cell_margins(row_cells[c_idx], top=100, bottom=100, left=140, right=140)
                p = row_cells[c_idx].paragraphs[0]
                p.alignment = WD_ALIGN_PARAGRAPH.LEFT if c_idx == 0 else WD_ALIGN_PARAGRAPH.CENTER
                if len(p.runs) > 0:
                    p.runs[0].font.name = 'Times New Roman'
                    p.runs[0].font.size = Pt(10)
                    p.runs[0].font.color.rgb = RGBColor(30, 41, 59)
                    if c_idx == 0:
                        p.runs[0].font.bold = True

        if col_widths:
            for row in table.rows:
                for idx, w in enumerate(col_widths):
                    row.cells[idx].width = Inches(w)

        doc.add_paragraph().paragraph_format.space_after = Pt(6)

    # ==========================================
    # 1. COVER PAGE
    # ==========================================
    add_p("A DISSERTATION ON", bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, space_before=24, space_after=12, font_size=12, color=RGBColor(100, 116, 139))
    add_p("AERIAL IMAGE SEGMENTATION FOR LAND USE CLASSIFICATION", bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, space_before=6, space_after=8, font_size=20, color=RGBColor(15, 23, 42))
    add_p("A Two-Tier Multimodal Vision AI Guardrail and Class-Balanced Self-Training Domain Adaptation Framework for Rugged Rural Terrain", italic=True, align=WD_ALIGN_PARAGRAPH.CENTER, space_before=4, space_after=32, font_size=13, color=RGBColor(51, 65, 85))

    add_p("Submitted in partial fulfillment of the requirements for the award of the degree of", align=WD_ALIGN_PARAGRAPH.CENTER, space_before=16, space_after=6, font_size=11, color=RGBColor(71, 85, 105))
    add_p("BACHELOR OF TECHNOLOGY\nIN\nCOMPUTER SCIENCE AND ENGINEERING", bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, space_before=6, space_after=36, font_size=13, color=RGBColor(30, 41, 59))

    # Two column layout for Student and Supervisor
    t_info = doc.add_table(rows=1, cols=2)
    t_info.alignment = WD_TABLE_ALIGNMENT.CENTER
    c_left = t_info.cell(0, 0)
    c_right = t_info.cell(0, 1)
    c_left.width = Inches(3.2)
    c_right.width = Inches(3.2)

    p_l = c_left.paragraphs[0]
    p_l.alignment = WD_ALIGN_PARAGRAPH.LEFT
    r = p_l.add_run("SUBMITTED BY:\n")
    r.bold = True
    r.font.size = Pt(10.5)
    r = p_l.add_run("ANIKET KUMAR\n")
    r.bold = True
    r.font.size = Pt(12)
    r.font.color.rgb = RGBColor(15, 23, 42)
    r = p_l.add_run("Enrollment No: BT23CS028\nDepartment of CSE")
    r.font.size = Pt(11)

    p_r = c_right.paragraphs[0]
    p_r.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    r = p_r.add_run("UNDER THE GUIDANCE OF:\n")
    r.bold = True
    r.font.size = Pt(10.5)
    r = p_r.add_run("Dr. TANMAY KUMAR BEHERA\n")
    r.bold = True
    r.font.size = Pt(12)
    r.font.color.rgb = RGBColor(15, 23, 42)
    r = p_r.add_run("Assistant Professor\nDepartment of CSE")
    r.font.size = Pt(11)

    add_p("", space_before=36, space_after=12)

    add_p("DEPARTMENT OF COMPUTER SCIENCE AND ENGINEERING\nNATIONAL INSTITUTE OF TECHNOLOGY MIZORAM\nAIZAWL, MIZORAM – 796012, INDIA", bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, space_before=24, space_after=0, font_size=12, color=RGBColor(15, 23, 42))

    doc.add_page_break()

    # ==========================================
    # 2. CERTIFICATE OF ENDORSEMENT
    # ==========================================
    add_p("NATIONAL INSTITUTE OF TECHNOLOGY MIZORAM", bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, space_before=12, space_after=2, font_size=14, color=RGBColor(15, 23, 42))
    add_p("Department of Computer Science and Engineering\nAizawl, Mizoram – 796012, India", align=WD_ALIGN_PARAGRAPH.CENTER, space_before=0, space_after=24, font_size=11, color=RGBColor(71, 85, 105))
    
    add_p("CERTIFICATE OF RECOMMENDATION", bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, space_before=12, space_after=20, font_size=15, color=RGBColor(15, 23, 42))

    add_p(
        "This is to certify that the dissertation entitled \"Aerial Image Segmentation for Land Use Classification: "
        "A Two-Tier Multimodal Vision AI Guardrail and Class-Balanced Self-Training Domain Adaptation Framework for Rugged Rural Terrain\", "
        "submitted by ANIKET KUMAR (Enrollment No. BT23CS028) in partial fulfillment of the requirements for the award of the degree of "
        "Bachelor of Technology in Computer Science and Engineering at the National Institute of Technology Mizoram, is an authentic record of "
        "bonafide research and technical work carried out under my supervision and guidance.",
        space_before=12, space_after=12
    )

    add_p(
        "To the best of my knowledge, the matter embodied in this dissertation has not been submitted in part or full to any other University or "
        "Institute for the award of any degree, diploma, or academic distinction.",
        space_before=6, space_after=36
    )

    t_cert = doc.add_table(rows=1, cols=2)
    t_cert.alignment = WD_TABLE_ALIGNMENT.CENTER
    c1 = t_cert.cell(0, 0)
    c2 = t_cert.cell(0, 1)
    c1.width = Inches(3.2)
    c2.width = Inches(3.2)

    p1 = c1.paragraphs[0]
    p1.alignment = WD_ALIGN_PARAGRAPH.LEFT
    p1.add_run("______________________________\n").bold = True
    p1.add_run("Dr. Tanmay Kumar Behera\n").bold = True
    p1.add_run("Supervisor / Assistant Professor\nDepartment of CSE\nNIT Mizoram")

    p2 = c2.paragraphs[0]
    p2.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    p2.add_run("______________________________\n").bold = True
    p2.add_run("Head of the Department\n").bold = True
    p2.add_run("Department of CSE\nNIT Mizoram")

    add_p("", space_before=24, space_after=12)

    p_ext = doc.add_paragraph()
    p_ext.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_ext.add_run("______________________________\n").bold = True
    p_ext.add_run("External Examiner\n(Board of Examiners)")

    doc.add_page_break()

    # ==========================================
    # 3. DECLARATION & ACKNOWLEDGMENTS
    # ==========================================
    add_h1("CANDIDATE'S DECLARATION")
    add_p(
        "I hereby declare that the work presented in this final-year B.Tech capstone project report entitled \"Aerial Image Segmentation for Land Use "
        "Classification\" is an authentic record of my own investigation carried out under the supervision of Dr. Tanmay Kumar Behera, Assistant Professor, "
        "Department of Computer Science and Engineering, National Institute of Technology Mizoram.",
        space_before=6, space_after=10
    )
    add_p(
        "I have adhered to all academic ethics and honesty standards. No portion of this technical report or code has been plagiarized, and all external "
        "literature, datasets, benchmarks, algorithms, and software libraries (including the LoveDA benchmark, DeepLabV3+ architecture, PyTorch, GDAL, "
        "and Google Gemini APIs) have been appropriately referenced and acknowledged.",
        space_before=6, space_after=24
    )
    p_dec = doc.add_paragraph()
    p_dec.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    p_dec.add_run("Aniket Kumar\n").bold = True
    p_dec.add_run("Enrollment No. BT23CS028\nB.Tech (Final Year), CSE\nNIT Mizoram, Aizawl")

    add_h1("ACKNOWLEDGMENTS")
    add_p(
        "I express my deepest gratitude to my project supervisor, Dr. Tanmay Kumar Behera, Assistant Professor, Department of Computer Science and "
        "Engineering, National Institute of Technology Mizoram, for his inspiring guidance, critical feedback, and constant encouragement throughout "
        "the conceptualization, mathematical formulation, and experimental execution of this research.",
        space_before=6, space_after=10
    )
    add_p(
        "I extend my sincere thanks to the Head of the Department and all faculty members of the Department of Computer Science and Engineering for "
        "providing the computational resources, laboratory facilities, and intellectual environment necessary to complete this project.",
        space_before=6, space_after=10
    )
    add_p(
        "Finally, I am profoundly grateful to my parents, family, and peers for their unwavering patience, support, and motivation throughout my undergraduate studies.",
        space_before=6, space_after=18
    )

    doc.add_page_break()

    # ==========================================
    # 4. ABSTRACT
    # ==========================================
    add_h1("ABSTRACT")
    add_p(
        "High-resolution aerial and satellite remote sensing enables automated land-cover mapping essential for environmental governance, urban planning, "
        "disaster resilience, and agricultural monitoring. However, contemporary deep convolutional semantic segmentation networks suffer catastrophic "
        "performance degradation when deployed across heterogeneous geospatial domains due to significant domain shift. In particular, deep models trained "
        "on structured, high-density urban aerial imagery fail drastically when applied to complex rural and montane environments—such as the rugged ridgelines, "
        "shifting Jhum cultivation plots, and unpaved corridors characteristic of Mizoram and Northeast India.",
        space_before=6, space_after=10
    )
    add_p(
        "In this dissertation, we present a robust, production-grade end-to-end framework that resolves this challenge through a novel two-tier architecture "
        "combining multimodal vision foundation intelligence with unsupervised domain adaptation. In Tier 1, an enterprise-grade Multimodal Vision AI "
        "(Google Gemini 1.5 Vision) serves as an operational gatekeeper and semantic guardrail, inspecting incoming orthophotos to verify orthogonal perspective "
        "validity, flag terrestrial/non-aerial corruptions, and identify macro-terrain contexts. In Tier 2, high-altitude aerial scenes are segmented using a "
        "DeepLabV3+ architecture with a ResNet-50 feature backbone and Atrous Spatial Pyramid Pooling (ASPP).",
        space_before=6, space_after=10
    )
    add_p(
        "To overcome the severe domain gap without requiring costly manual pixel annotations on rural terrain, we implement Class-Balanced Self-Training (CBST). "
        "CBST adaptively calculates class-specific confidence thresholds ($\lambda_c$) to extract high-confidence pseudo-labels from unlabeled target imagery, "
        "effectively preventing majority classes from dominating gradient updates. Experimental benchmarking on the rigorous LoveDA Land-Cover dataset reveals "
        "that direct cross-domain transfer experiences a steep 15.55% mIoU domain penalty (dropping from 38.93% on urban source data to 23.39% on rural target data). "
        "Following CBST domain adaptation, our model achieves 27.90% mIoU, delivering a net improvement of +4.52% mIoU (+19.31% relative gain). Crucially, "
        "sparse and critical rural classes experience dramatic recoveries: Road IoU surges by +11.27% (from 20.03% to 31.30%), Water IoU increases by +7.95% "
        "(from 38.21% to 46.15%), and Agriculture increases by +5.88% (from 42.31% to 48.19%). Validation across 992 high-resolution GeoTIFF rasters confirms "
        "29.57% calibrated raster mIoU.",
        space_before=6, space_after=10
    )
    add_p(
        "Furthermore, we bridge machine learning research and practical GIS governance by developing a full-stack, cloud-deployed web portal "
        "(React 19, Node.js/Express, Python FastAPI, MongoDB Atlas, Dockerized and hosted on Render) that performs real-time pixel-to-hectare land-use quantification "
        "using sub-meter Ground Sampling Distance (GSD) calculus.",
        space_before=6, space_after=10
    )
    add_p(
        "Keywords: Aerial Image Segmentation, DeepLabV3+, Unsupervised Domain Adaptation, Class-Balanced Self-Training (CBST), Geospatial Analytics, "
        "Multimodal Vision AI Guardrail, LoveDA Benchmark, Mizoram Remote Sensing.",
        bold=True, italic=True, space_before=10, space_after=18
    )

    doc.add_page_break()

    # ==========================================
    # 5. TABLE OF CONTENTS & LIST OF TABLES/FIGURES
    # ==========================================
    add_h1("TABLE OF CONTENTS")
    toc_data = [
        ("1. INTRODUCTION & PROBLEM DEFINITION", "1"),
        ("   1.1 Background and Significance of Aerial Remote Sensing", "1"),
        ("   1.2 Topographic Challenges of Mizoram & Northeast India", "2"),
        ("   1.3 The Domain Shift Problem in Remote Sensing", "3"),
        ("   1.4 Project Objectives and Key Contributions", "4"),
        ("   1.5 Dissertation Organization", "5"),
        ("2. LITERATURE REVIEW & RELATED WORK", "6"),
        ("   2.1 Deep Learning Architectures for Semantic Segmentation", "6"),
        ("   2.2 Atrous Convolutions and Spatial Pyramid Pooling (ASPP)", "7"),
        ("   2.3 Unsupervised Domain Adaptation (UDA) Frameworks", "8"),
        ("   2.4 Class-Balanced Self-Training (CBST) Foundations", "9"),
        ("   2.5 Multimodal Vision-Language Models as System Guardrails", "10"),
        ("3. DATASET ARCHITECTURE & GEOSPATIAL METHODOLOGY", "11"),
        ("   3.1 The LoveDA Remote Sensing Benchmark", "11"),
        ("   3.2 Seven-Class Land-Cover Taxonomy", "12"),
        ("   3.3 Spectral Feature Proxies (NDVI, ExG, NDWI)", "13"),
        ("   3.4 Ground Sampling Distance & Metric Hectare Calculus", "14"),
        ("4. METHODOLOGY & DEEP LEARNING ARCHITECTURE", "15"),
        ("   4.1 Two-Tier System Architecture Overview", "15"),
        ("   4.2 Tier-1: Multimodal Vision AI Domain Gatekeeper", "16"),
        ("   4.3 Tier-2: DeepLabV3+ with ResNet-50 Feature Backbone", "17"),
        ("   4.4 Atrous Spatial Pyramid Pooling (ASPP) Details", "18"),
        ("   4.5 Low-Level Feature Fusion Decoder & Upsampling", "19"),
        ("   4.6 Loss Formulation and Optimization Protocol", "20"),
        ("5. UNSUPERVISED DOMAIN ADAPTATION VIA CBST", "21"),
        ("   5.1 Mathematical Formulation of Self-Training", "21"),
        ("   5.2 Class-Specific Confidence Threshold Selection", "22"),
        ("   5.3 Hard Pseudo-Label Generation and Filtering", "23"),
        ("   5.4 Preventing Minority Class Starvation", "24"),
        ("6. EXPERIMENTAL SETUP & TRAINING METHODOLOGY", "25"),
        ("   6.1 Hardware and Compute Infrastructure", "25"),
        ("   6.2 Training Protocols and Hyperparameter Configuration", "26"),
        ("   6.3 Quantitative Evaluation Metrics", "27"),
        ("7. RESULTS, ABLATION STUDIES & DISCUSSION", "28"),
        ("   7.1 Source Domain Benchmark Performance (Urban)", "28"),
        ("   7.2 Target Domain Baseline Performance (Direct Transfer)", "29"),
        ("   7.3 CBST Domain Adaptation Gains", "30"),
        ("   7.4 Detailed Class-Wise IoU Recovery Analysis", "31"),
        ("   7.5 Validation Across 992 Full-Scale GeoTIFF Rasters", "32"),
        ("   7.6 Qualitative Visual Comparisons & Error Analysis", "33"),
        ("8. FULL-STACK CLOUD APPLICATION & PRODUCTION DEPLOYMENT", "35"),
        ("   8.1 End-to-End System Architecture", "35"),
        ("   8.2 Docker Single-Container Orchestration", "36"),
        ("   8.3 Real-Time GIS Hectare Surface Area Calculation Engine", "37"),
        ("   8.4 Live Cloud Deployment on Render", "38"),
        ("9. CONCLUSION, SOCIETAL IMPACT & FUTURE WORK", "39"),
        ("   9.1 Summary of Contributions", "39"),
        ("   9.2 Practical Applications for Governance in Mizoram", "40"),
        ("   9.3 Future Research Directions", "41"),
        ("REFERENCES", "42"),
        ("APPENDIX: MATHEMATICAL FORMULATIONS & SOURCE CODE", "45")
    ]
    for title, pg in toc_data:
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(1)
        p.paragraph_format.space_after = Pt(2)
        r1 = p.add_run(title)
        r1.font.name = 'Times New Roman'
        r1.font.size = Pt(10.5)
        if title.startswith(("1.", "2.", "3.", "4.", "5.", "6.", "7.", "8.", "9.", "REF", "APP")):
            r1.bold = True
        # Dot leader
        r2 = p.add_run(f"  {pg}")
        r2.font.name = 'Times New Roman'
        r2.font.size = Pt(10.5)

    doc.add_page_break()

    # ==========================================
    # CHAPTER 1: INTRODUCTION
    # ==========================================
    add_h1("CHAPTER 1: INTRODUCTION & PROBLEM DEFINITION")
    add_h2("1.1 Background and Significance of Aerial Remote Sensing")
    add_p(
        "Earth observation and aerial remote sensing have undergone a transformative paradigm shift with the rapid convergence of high-resolution "
        "spaceborne sensors, Unmanned Aerial Vehicles (UAVs), and deep convolutional neural networks. Modern optical sensors acquire high-resolution "
        "orthophotos with Ground Sampling Distances (GSD) beneath 0.5 meters per pixel, uncovering fine-grained geometric details ranging from individual "
        "building rooflines to narrow transport corridors and minor riparian waterways. Extracting accurate, pixel-level land-use and land-cover (LULC) maps "
        "from these complex aerial images is indispensable for urban planning, hydrological basin modeling, automated disaster damage assessment, and "
        "forest conservation.",
        space_before=4, space_after=8
    )

    add_h2("1.2 Topographic Challenges of Mizoram & Northeast India")
    add_p(
        "While computer vision models achieve state-of-the-art segmentation benchmark scores on standardized metropolitan datasets (e.g. European and East Asian "
        "megacities), deploying these models in rural, montane geographies introduces severe domain failure. The state of Mizoram, nestled in the southern "
        "reach of Northeast India, exemplifies these extreme challenges. Characterized by parallel north-south oriented hill ridges, steep valley gorges, "
        "dense subtropical evergreen forests, and pervasive 'Jhum' (slash-and-burn shifting cultivation) agro-forestry cycles, Mizoram's terrain differs "
        "fundamentally from rectilinear urban environments.",
        space_before=4, space_after=8
    )
    add_p(
        "In rural Mizoram, transport infrastructure consists primarily of sinuous, unpaved or cut-slope roadways that visually blend into flanking barren "
        "earth or scrub vegetation. Settlements comprise scattered clusters of tin-roofed and bamboo dwellings clinging to ridge spurs rather than uniform "
        "concrete street grids. Furthermore, agricultural plots in Mizoram undergo rapid seasonal transitions from cleared barren slopes to active green crops, "
        "producing intense intra-class spectral variance.",
        space_before=4, space_after=8
    )

    add_h2("1.3 The Domain Shift Problem in Remote Sensing")
    add_p(
        "When a deep semantic segmentation model trained on annotated urban orthophotos ($P_{source}(X, Y)$) is directly evaluated on target rural imagery "
        "($P_{target}(X)$), a catastrophic drop in mean Intersection-over-Union (mIoU) occurs. This phenomenon—termed domain shift—is driven by discrepancies "
        "in both marginal image distributions $P(X)$ (e.g. differing illumination, spectral reflectance, atmospheric scatter, sensor GSD) and conditional distributions "
        "$P(Y|X)$ (e.g. structural differences where 'road' manifests as rectilinear asphalt in the source domain but irregular dirt tracks in the target domain).",
        space_before=4, space_after=8
    )
    add_callout(
        "In our empirical experiments, evaluating a high-performing Urban-trained DeepLabV3+ model directly on Rural aerial imagery resulted in a catastrophic "
        "15.55% mIoU drop (from 38.93% down to 23.39%). In particular, Road segmentation collapsed by 24.87% and Forest segmentation plummeted by 23.83%, "
        "rendering the direct transfer model operationally unusable without domain adaptation.",
        prefix="THE DOMAIN GAP PENALTY:"
    )

    add_h2("1.4 Project Objectives and Key Contributions")
    add_p(
        "To resolve the dual challenge of domain shift and operational robustness, this B.Tech capstone project establishes the following core objectives:",
        space_before=4, space_after=6
    )
    add_p("1. Formulate a Two-Tier Hybrid Architecture integrating multimodal foundation model guardrails (Google Gemini 1.5 Vision) with deep segmentation backbones to prevent out-of-domain corrupted inference.", space_after=4)
    add_p("2. Implement and optimize DeepLabV3+ with ResNet-50 and Atrous Spatial Pyramid Pooling (ASPP) to capture multi-scale context across complex rural land forms.", space_after=4)
    add_p("3. Design and execute Class-Balanced Self-Training (CBST) unsupervised domain adaptation to adapt the source-trained urban model to target rural terrain without requiring manual pixel labels.", space_after=4)
    add_p("4. Conduct rigorous ablation and validation across 992 high-resolution validation GeoTIFF rasters.", space_after=4)
    add_p("5. Architect and deploy a live, production-grade cloud application (MERN + FastAPI + GDAL + Docker on Render) providing instantaneous sub-meter hectare quantification for real-world governance.", space_after=12)

    doc.add_page_break()

    # ==========================================
    # CHAPTER 2: LITERATURE REVIEW
    # ==========================================
    add_h1("CHAPTER 2: LITERATURE REVIEW & RELATED WORK")
    add_h2("2.1 Semantic Segmentation in Remote Sensing")
    add_p(
        "Semantic segmentation assigns a discrete categorical semantic label to each individual pixel in an input image. Early remote sensing pipelines "
        "relied on manual feature engineering, such as spectral angle mappers, Support Vector Machines (SVM), and Random Forests operating on normalized "
        "indices (NDVI, NDWI). The advent of deep Convolutional Neural Networks (CNNs) revolutionized the field. Long et al. (2015) introduced Fully "
        "Convolutional Networks (FCN), replacing dense classification layers with convolutional transpose operations to output spatial heatmaps. "
        "Ronneberger et al. (2015) advanced biomedical and satellite segmentation with U-Net, introducing symmetric contracting and expanding paths bridged "
        "by skip connections that preserve high-frequency spatial boundary information.",
        space_before=4, space_after=8
    )

    add_h2("2.2 DeepLabV3+ and Atrous Spatial Pyramid Pooling (ASPP)")
    add_p(
        "Standard convolutional downsampling (strided convolutions, max-pooling) inherently degrades spatial feature resolution, causing fine structural details "
        "(such as secondary roads and small rural houses) to be lost. Chen et al. (2017, 2018) addressed this fundamental trade-off through atrous (dilated) "
        "convolutions. By inserting holes into convolution kernels, atrous convolutions expand the effective receptive field without increasing parameter count "
        "or reducing spatial grid resolution. DeepLabV3+ introduces Atrous Spatial Pyramid Pooling (ASPP), applying multiple parallel atrous convolutions with "
        "dilations $r \in \{6, 12, 18\}$ alongside global average pooling, capturing multi-scale context ranging from broad forest canopies to narrow roads.",
        space_before=4, space_after=8
    )

    add_h2("2.3 Unsupervised Domain Adaptation (UDA) in Remote Sensing")
    add_p(
        "Unsupervised Domain Adaptation (UDA) addresses scenarios where labeled source data $D_s = \{(x_i^s, y_i^s)\}$ is abundant, but target data $D_t = \{x_j^t\}$ "
        "lacks ground-truth annotations. Traditional UDA methods employ adversarial feature alignment (Ganin et al., 2016; Tsai et al., 2018; AdaptSegNet), "
        "wherein a domain discriminator is trained to distinguish source features from target features while the segmentation backbone learns domain-invariant "
        "representations via minimax games. However, adversarial alignment often suffers from training instability, mode collapse, and feature distortion on "
        "fine-grained remote sensing classes.",
        space_before=4, space_after=8
    )

    add_h2("2.4 Class-Balanced Self-Training (CBST)")
    add_p(
        "Self-training has emerged as an exceptionally effective alternative to adversarial alignment (Zou et al., 2018). In standard pseudo-labeling, "
        "target predictions surpassing a fixed threshold $\tau$ (e.g. 0.9) are treated as pseudo-ground truth. However, remote sensing datasets suffer from "
        "severe class imbalance: ubiquitous categories (e.g. Forest, Agriculture) easily attain high confidence and monopolize pseudo-labels, while minority "
        "categories (e.g. Roads, Barren, Buildings) are completely starved of training signal. Class-Balanced Self-Training (CBST) resolves this imbalance by "
        "dynamically optimizing class-specific thresholds $\lambda_c$ such that top portions of pseudo-labels are preserved proportionally across all categories.",
        space_before=4, space_after=12
    )

    # Table of Related Works
    headers_lit = ["Architecture / Framework", "Core Mechanism", "Primary Advantage", "Observed Limitation in Remote Sensing"]
    rows_lit = [
        ["FCN-8s (Long et al.)", "Skip-layer feature combination", "End-to-end pixel classification", "Coarse boundary predictions; lacks multi-scale context"],
        ["U-Net (Ronneberger et al.)", "Symmetric encoder-decoder + skips", "Precise edge and shape recovery", "Over-reliant on local cues; prone to large-scale context errors"],
        ["AdaptSegNet (Tsai et al.)", "Adversarial output space alignment", "Domain-invariant representations", "High training instability; fails on skewed class distributions"],
        ["DeepLabV3+ (Chen et al.)", "ASPP + Dilated Convolutions", "Superior multi-scale feature capture", "Severe performance drop under cross-domain distribution shifts"],
        ["Our Proposed Framework", "Two-Tier Gemini Guardrail + CBST", "Robust gatekeeper + class-balanced UDA", "Requires multi-stage iterative retraining"]
    ]
    add_styled_table(headers_lit, rows_lit, [1.5, 1.6, 1.7, 1.7])

    doc.add_page_break()

    # ==========================================
    # CHAPTER 3: DATASET ARCHITECTURE
    # ==========================================
    add_h1("CHAPTER 3: DATASET ARCHITECTURE & GEOSPATIAL METHODOLOGY")
    add_h2("3.1 The LoveDA Remote Sensing Benchmark")
    add_p(
        "To rigorously evaluate domain shift under real-world conditions, we employ the Land-Cover Domain Adaptive (LoveDA) benchmark dataset (Wang et al., 2021). "
        "Acquired across three major metropolitan and rural geographical zones in China (Nanjing, Changzhou, Wuhan) using high-altitude aerial platforms, "
        "LoveDA comprises 5,987 total high-resolution image patches of dimension $1024 \times 1024$ pixels at a spatial resolution (Ground Sampling Distance) of 0.3 meters per pixel.",
        space_before=4, space_after=8
    )
    add_p(
        "LoveDA is explicitly designed to test cross-domain transfer. It features two clearly bifurcated domains:",
        space_before=4, space_after=4
    )
    add_p("• Urban Domain (Source): High-density commercial and residential regions characterized by multi-story buildings, paved multi-lane highway networks, structured waterways, and manicured parks.", space_after=4)
    add_p("• Rural Domain (Target): Complex rural basins characterized by small agricultural villages, unpaved secondary roads, natural drainage canals, rugged forest slopes, and terraced farmlands—closely matching Mizoram's rural landscape.", space_after=8)

    add_h2("3.2 Seven-Class Land-Cover Taxonomy")
    add_p(
        "The benchmark enforces an official 7-class mutually exclusive land-cover taxonomy. Table 3.1 details the class IDs, color representations, and geospatial definitions.",
        space_before=4, space_after=6
    )

    headers_tax = ["Class ID", "Class Name", "Hex Color Code", "RGB Palette", "Geospatial Definition in Rural Mizoram Context"]
    rows_tax = [
        ["0", "Background", "#2A2A2A", "[42, 42, 42]", "Unclassified regions, clouds, sensor shadows, out-of-boundary pixels"],
        ["1", "Building", "#EF4444", "[239, 68, 68]", "Residential homes, agricultural storehouses, tin-roofed dwellings"],
        ["2", "Road", "#EAB308", "[234, 179, 8]", "Paved highways, cut-slope hillside corridors, unpaved village tracks"],
        ["3", "Water", "#3B82F6", "[59, 130, 246]", "Rivers, mountain streams, irrigation retention ponds, alluvial channels"],
        ["4", "Barren", "#A855F7", "[168, 85, 247]", "Exposed rock spurs, landslide scars, cleared soil, excavation zones"],
        ["5", "Forest", "#22C55E", "[34, 197, 94]", "Dense subtropical evergreen forest, bamboo groves, protected hill canopy"],
        ["6", "Agriculture", "#F97316", "[249, 115, 22]", "Terraced hill crops, valley rice paddies, active Jhum cultivation parcels"]
    ]
    add_styled_table(headers_tax, rows_tax, [0.8, 1.1, 1.1, 1.2, 2.3])

    add_h2("3.3 Spectral Feature Proxies (NDVI, ExG, NDWI)")
    add_p(
        "To enable resilient fallback segmentation when deep neural network weights are offline or computationally constrained, we formulated an adaptive "
        "spectral proxy engine. Using calibrated Red ($R$), Green ($G$), and Blue ($B$) reflectance values, we compute spectral indices:",
        space_before=4, space_after=6
    )
    add_p("1. Excess Green Index (ExG): Quantifies photosynthetic vegetation density across forest and agriculture:", space_after=2)
    add_p("    ExG = (2 · G - R - B) / (R + G + B + 10⁻⁵)", italic=True, space_after=4)
    add_p("2. Water Reflectance Proxy (NDWI Proxy): Detects low-reflectance, blue-dominant hydrological features:", space_after=2)
    add_p("    W_idx = (B - R) / (B + R + 10⁻⁵)", italic=True, space_after=4)
    add_p("3. Redness Roof Index: Separates clay and red tin roofs from natural soil and barren ground:", space_after=2)
    add_p("    Red_idx = (R - G) / (R + G + 10⁻⁵)", italic=True, space_after=8)

    add_h2("3.4 Ground Sampling Distance & Metric Hectare Calculus")
    add_p(
        "A critical innovation in our framework is the real-world metric conversion engine. In high-resolution remote sensing, each pixel represents a calibrated "
        "physical ground area determined by the Ground Sampling Distance ($GSD$ in meters/pixel):",
        space_before=4, space_after=4
    )
    add_p("    Pixel Area (m²) = GSD × GSD", italic=True, space_after=4)
    add_p("    Class Area (Hectares) = (Pixel Count × GSD²) / 10,000", italic=True, space_after=8)
    add_p(
        "For standard LoveDA orthophotos ($1024 \times 1024$ pixels at $GSD = 0.3$ m/pixel), each pixel covers exactly $0.09$ m², yielding a total tile ground "
        "footprint of $94,371.84$ m² (9.4372 Hectares). This mathematical formulation enables municipal authorities to obtain instant, legally actionable land-use totals.",
        space_before=4, space_after=12
    )

    doc.add_page_break()

    # ==========================================
    # CHAPTER 4: METHODOLOGY & DEEP LEARNING ARCHITECTURE
    # ==========================================
    add_h1("CHAPTER 4: METHODOLOGY & DEEP LEARNING ARCHITECTURE")
    add_h2("4.1 Two-Tier System Architecture Overview")
    add_p(
        "Conventional deep segmentation pipelines directly ingest raw uploaded imagery without verifying operational suitability. When users inadvertently "
        "upload non-aerial images (e.g. ground-level selfies, indoor rooms, scanned documents) or corrupt sensor files, deep models produce catastrophic, "
        "nonsensical land-use segmentations. To eliminate this operational vulnerability, our framework introduces a Two-Tier Architecture:",
        space_before=4, space_after=8
    )
    add_p("• Tier 1 (Semantic Domain Gatekeeper): Multimodal Gemini 1.5 Vision AI assesses the input image, verifying orthogonal orientation, valid aerial perspective, and expected land-cover features.", space_after=4)
    add_p("• Tier 2 (DeepLand-Cover Segmentation): DeepLabV3+ with ResNet-50 and ASPP performs pixel-level semantic segmentation and GDAL metric quantification.", space_after=12)

    add_fig("side_by_side_comparison.png", "Figure 4.1: End-to-End Visual Pipeline: Input Orthophoto, Ground Truth Annotation, and Final Domain-Adapted Prediction.")

    add_h2("4.2 Tier-1: Multimodal Vision AI Domain Gatekeeper")
    add_p(
        "The Tier-1 gatekeeper utilizes Google Gemini 1.5 Vision with a temperature parameter of 0.1 and strict JSON schema enforcement. The model evaluates "
        "whether the input is an orthogonal aerial or satellite orthophoto, extracts visible land-cover categories, and assigns a confidence score $S \in [0, 1]$. "
        "If $S < 0.85$ or out-of-domain keywords (e.g. terrestrial, indoor, macro) are detected, the system issues an HTTP 422 Unprocessable Entity response, "
        "preventing Tier-2 GPU processing and protecting municipal decision-makers from flawed analytical outputs.",
        space_before=4, space_after=8
    )

    add_h2("4.3 DeepLabV3+ Encoder-Decoder Architecture")
    add_p(
        "The segmentation core implements DeepLabV3+ utilizing a ResNet-50 backbone initialized with ImageNet pre-trained weights. ResNet-50 comprises 53 "
        "convolutional layers organized into 4 residual stages. In stages 3 and 4, standard downsampling strides are modified to atrous convolutions with "
        "output stride $OS = 16$, preserving high-level semantic representation without forfeiting spatial coordinate fidelity.",
        space_before=4, space_after=8
    )
    add_p(
        "The extracted feature map is passed through the Atrous Spatial Pyramid Pooling (ASPP) module, which applies 5 parallel branches:",
        space_before=4, space_after=4
    )
    add_p("1. One $1 \times 1$ standard convolution (256 channels).", space_after=2)
    add_p("2. Three $3 \times 3$ atrous convolutions with expansion rates $r = \{6, 12, 18\}$ (256 channels each).", space_after=2)
    add_p("3. Image-level Global Average Pooling with $1 \times 1$ convolution and bilinear upsampling.", space_after=4)
    add_p(
        "The outputs are concatenated into a 1280-channel tensor and compressed through a $1 \times 1$ convolution to 256 channels. In the decoder, low-level "
        "features from ResNet stage 1 are passed through a $1 \times 1$ projection (48 channels) to balance gradient flow and fused with the ASPP features, "
        "followed by $3 \times 3$ convolutions and $4\times$ bilinear upsampling to reconstruct the original $1024 \times 1024$ spatial mask.",
        space_before=4, space_after=12
    )

    doc.add_page_break()

    # ==========================================
    # CHAPTER 5: UNSUPERVISED DOMAIN ADAPTATION VIA CBST
    # ==========================================
    add_h1("CHAPTER 5: UNSUPERVISED DOMAIN ADAPTATION VIA CBST")
    add_h2("5.1 Mathematical Formulation of Class-Balanced Self-Training")
    add_p(
        "Let $X_s = \{x_i^s\}_{i=1}^{N_s}$ denote labeled source urban images with ground-truth masks $Y_s = \{y_i^s\}_{i=1}^{N_s}$, where $y_i^s(u, v) \in \{1, \dots, C\}$. "
        "Let $X_t = \{x_j^t\}_{j=1}^{N_t}$ denote unlabeled target rural images. The baseline model is trained by minimizing the empirical source cross-entropy loss:",
        space_before=4, space_after=6
    )
    add_p("    L_s(w) = - (1 / N_s) ∑_{i=1}^{N_s} ∑_{u,v} log P(y_i^s(u, v) | x_i^s; w)", italic=True, space_after=8)
    add_p(
        "In self-training, the model generates soft probability distributions $P_c(u, v) = \text{softmax}(z_c(u, v))$ on unlabeled target images $x_j^t$. "
        "To select pseudo-labels without succumbing to class imbalance, CBST defines an optimization objective over model parameters $w$ and latent pseudo-labels $\hat{y}$:",
        space_before=4, space_after=6
    )
    add_p("    min_{w, \hat{y}} L(w, \hat{y}) = L_s(w) - ∑_{j=1}^{N_t} ∑_{u,v} ∑_{c=1}^C \hat{y}_{j,c}(u, v) log( P_c(u, v | x_j^t; w) / λ_c )", italic=True, space_after=8)

    add_h2("5.2 Class-Specific Threshold Selection (λ_c)")
    add_p(
        "Rather than imposing a single global confidence cutoff (which causes frequent classes like Forest to capture 95% of pseudo-labels while Road captures 0%), "
        "CBST adaptively determines class-specific thresholds $\lambda_c$. For each class $c$, the system ranks all predicted probabilities $P_c$ across the target corpus "
        "and sets $\lambda_c$ such that a fixed proportion $p_c \in (0, 1]$ of top candidate pixels are selected:",
        space_before=4, space_after=6
    )
    add_p("    λ_c = \text{Percentile}( \{ P_c(u, v | x_j^t) \}, 1 - p_c )", italic=True, space_after=8)
    add_p(
        "Hard pseudo-labels $\hat{y}_{j}(u, v)$ are then assigned to the class maximizing the normalized confidence ratio:",
        space_before=4, space_after=6
    )
    add_p("    \hat{y}_{j}(u, v) = \text{argmax}_c [ P_c(u, v | x_j^t) / λ_c ]  \quad \text{if} \quad \max_c [ P_c(u, v) / λ_c ] ≥ 1", italic=True, space_after=8)
    add_p(
        "If no class satisfies the condition, the pixel is marked as 0 (ignored in backpropagation). This rigorous formulation guarantees that minority categories "
        "(such as secondary roads and small farm structures in Mizoram) receive substantial pseudo-label representation, preventing gradient starvation and model collapse.",
        space_before=4, space_after=12
    )

    doc.add_page_break()

    # ==========================================
    # CHAPTER 6: EXPERIMENTAL SETUP
    # ==========================================
    add_h1("CHAPTER 6: EXPERIMENTAL SETUP & TRAINING METHODOLOGY")
    add_h2("6.1 Hardware and Compute Infrastructure")
    add_p(
        "Model training, adaptation loops, and ablation evaluations were conducted using PyTorch 2.0 with CUDA 11.8 on NVIDIA Tesla T4 GPUs (16 GB VRAM) "
        "under Google Colab Pro infrastructure, augmented with high-RAM system nodes (51 GB RAM). Standalone microservice deployment and cloud containerization "
        "were implemented using Docker on Render Cloud nodes running Python 3.11 and Node.js 20.",
        space_before=4, space_after=8
    )

    add_h2("6.2 Training Hyperparameters & Optimization Protocol")
    add_p(
        "The model was optimized using AdamW with weight decay $1 \times 10^{-4}$ and an initial learning rate $\eta_0 = 1 \times 10^{-4}$ governed by a "
        "polynomial learning rate decay schedule:",
        space_before=4, space_after=6
    )
    add_p("    η(t) = η_0 · (1 - t / T_max)^0.9", italic=True, space_after=8)

    headers_hp = ["Hyperparameter Name", "Baseline Source Training", "CBST Adaptation Stage", "Justification & Impact"]
    rows_hp = [
        ["Optimizer", "AdamW", "AdamW", "Decoupled weight decay prevents overfitting on high-frequency noise"],
        ["Initial Learning Rate", "1.0 × 10⁻⁴", "2.5 × 10⁻⁵", "Lower learning rate prevents catastrophic forgetting of source features"],
        ["LR Decay Policy", "Polynomial (power=0.9)", "Polynomial (power=0.9)", "Smooth convergence towards global minima"],
        ["Batch Size", "8 patches", "4 patches (due to dual pass)", "Maximizes GPU VRAM utilization for 1024×1024 images"],
        ["Input Resolution", "1024 × 1024 pixels", "1024 × 1024 pixels", "Preserves native LoveDA sub-meter GSD spatial resolution"],
        ["Data Augmentations", "H-Flip, V-Flip, ShiftScaleRotate", "H-Flip, V-Flip, ColorJitter", "Enforces rotational and illumination invariance in montane terrain"],
        ["CBST Target Ratio (p_c)", "N/A", "0.20 → 0.35 (progressive)", "Prevents early pseudo-label drift while scaling supervision"]
    ]
    add_styled_table(headers_hp, rows_hp, [1.5, 1.4, 1.4, 2.1])

    add_h2("6.3 Quantitative Evaluation Metrics")
    add_p(
        "Semantic segmentation performance is quantified across all categories using the standard Intersection-over-Union (IoU) metric (Jaccard Index) "
        "and Mean Intersection-over-Union (mIoU):",
        space_before=4, space_after=6
    )
    add_p("    IoU_c = TP_c / (TP_c + FP_c + FN_c)", italic=True, space_after=4)
    add_p("    mIoU = (1 / C) ∑_{c=1}^C IoU_c", italic=True, space_after=8)
    add_p(
        "where $TP_c$, $FP_c$, and $FN_c$ denote the True Positives, False Positives, and False Negatives for class $c$. In accordance with LoveDA official benchmark "
        "standards, Class 0 (Background) is excluded from mIoU calculation to ensure metrics reflect substantive land-cover categories.",
        space_before=4, space_after=12
    )

    doc.add_page_break()

    # ==========================================
    # CHAPTER 7: RESULTS ANALYSIS & ABLATION
    # ==========================================
    add_h1("CHAPTER 7: RESULTS, ABLATION STUDIES & DISCUSSION")
    add_h2("7.1 Domain Shift Discrepancy (Urban vs Rural)")
    add_p(
        "Our empirical investigation reveals an acute domain discrepancy between Urban and Rural aerial distributions. Table 7.1 establishes the quantified "
        "domain gap across all individual land-cover classes.",
        space_before=4, space_after=8
    )

    headers_gap = ["Land-Cover Class", "Source Domain IoU (Urban)", "Direct Transfer IoU (Rural)", "Absolute Domain Drop (Δ)", "Relative Drop (%)"]
    rows_gap = [
        ["Building", "43.54%", "22.96%", "-20.58%", "-47.27%"],
        ["Road", "44.90%", "20.03%", "-24.87%", "-55.39%"],
        ["Water", "55.57%", "38.21%", "-17.36%", "-31.24%"],
        ["Barren", "4.84%", "2.15%", "-2.69%", "-55.58%"],
        ["Forest", "38.48%", "14.65%", "-23.83%", "-61.93%"],
        ["Agriculture", "46.27%", "42.31%", "-3.96%", "-8.56%"],
        ["OVERALL mIoU", "38.93%", "23.39%", "-15.55%", "-39.94%"]
    ]
    add_styled_table(headers_gap, rows_gap, [1.4, 1.2, 1.2, 1.3, 1.3])

    add_fig("cbst_comparison_bar.png", "Figure 7.1: Comparative Analysis: Baseline Direct Transfer vs. CBST Domain Adapted Model Across All Classes.")

    add_h2("7.2 CBST Domain Adaptation Gains")
    add_p(
        "Applying Class-Balanced Self-Training successfully recovers from the severe domain gap. Table 7.2 presents the conclusive performance transformation "
        "achieved by our CBST adaptation framework.",
        space_before=4, space_after=8
    )

    headers_cbst = ["Land-Cover Class", "Baseline Rural IoU", "CBST Adapted Rural IoU", "Net Absolute Gain (Δ)", "Relative Improvement (%)"]
    rows_cbst = [
        ["Building", "22.96%", "22.40%", "-0.56%", "-2.44%"],
        ["Road", "20.03%", "31.30%", "+11.27%", "+56.27% (SURGE)"],
        ["Water", "38.21%", "46.15%", "+7.95%", "+20.80%"],
        ["Barren", "2.15%", "1.39%", "-0.76%", "-35.35%"],
        ["Forest", "14.65%", "17.97%", "+3.32%", "+22.66%"],
        ["Agriculture", "42.31%", "48.19%", "+5.88%", "+13.90%"],
        ["RURAL mIoU", "23.39%", "27.90%", "+4.52%", "+19.31% GAIN"]
    ]
    add_styled_table(headers_cbst, rows_cbst, [1.4, 1.2, 1.2, 1.3, 1.3])

    add_callout(
        "CBST adaptation achieved a dramatic breakthrough on the Road category, boosting IoU from 20.03% to 31.30%—a remarkable +56.27% relative surge. "
        "In rural and mountainous terrains like Mizoram, unpaved secondary corridors are routinely misclassified as barren soil by standard models. "
        "Class-balanced thresholding forced the model to extract high-confidence road segments, resolving road continuity across valley corridors.",
        prefix="CRITICAL BREAKTHROUGH ON TRANSPORT CORRIDORS:"
    )

    add_h2("7.3 Geospatial Validation on 992 Full-Scale GeoTIFF Rasters")
    add_p(
        "To guarantee that experimental results were not confined to isolated image crops, we executed batch inference across the complete LoveDA Rural "
        "Validation set comprising 992 full-scale $1024 \times 1024$ GeoTIFF rasters. Across all 992 evaluated spatial rasters (exceeding 1.04 billion total pixels), "
        "our adapted model attained an exceptional 29.57% raster mIoU, corroborating the stability and scalability of the segmentation engine.",
        space_before=4, space_after=12
    )

    add_fig("slide_segmentation_gallery_16x9.png", "Figure 7.2: Qualitative Benchmark Gallery Across Rural Test Scenes: Input RGB, Color-Coded Prediction, and Ground Truth.")

    add_fig("mizoram_landuse_pie.png", "Figure 7.3: Rural Land-Use Distribution Quantification Across Mizoram Test Terrain.")

    doc.add_page_break()

    # ==========================================
    # CHAPTER 8: FULL-STACK APPLICATION & PRODUCTION
    # ==========================================
    add_h1("CHAPTER 8: FULL-STACK CLOUD APPLICATION & PRODUCTION DEPLOYMENT")
    add_h2("8.1 System Architecture Overview")
    add_p(
        "To deliver actionable utility to GIS officers, environmental planners, and municipal engineers in Mizoram, we engineered and deployed a complete, "
        "production-grade full-stack web application. The platform adheres to modern microservices architecture, combining an ultra-responsive React 19 "
        "Single-Page Application (SPA), an enterprise Express.js API gateway, a high-throughput Python FastAPI machine learning microservice, and a cloud MongoDB Atlas database.",
        space_before=4, space_after=8
    )

    headers_arch = ["Component Layer", "Technology Stack", "Port & Runtime", "Functional Responsibilities"]
    rows_arch = [
        ["Client (Frontend)", "React 19, Vite, Tailwind CSS, Lucide Icons", "Served via Express static asset engine", "Interactive visual split comparison, real-time GSD slider, interactive donut charts, history drawer"],
        ["API Gateway (Backend)", "Node.js 20, Express.js, Multer, Mongoose", "Port 10000 (Render external edge)", "Request orchestration, Tier-1 Gemini Vision AI invocation, MongoDB history persistence, rate limiting"],
        ["ML Microservice", "Python 3.11, FastAPI, PyTorch, PIL, NumPy", "Port 8000 (Internal loopback)", "DeepLabV3+ ResNet-50 inference, spectral proxy classifier, single-band GeoTIFF raster encoding"],
        ["Database Layer", "MongoDB Atlas (M0 Shared Cluster)", "Cloud Hosted (yi4ir.mongodb.net)", "Persistent audit trail, scan telemetry, land-cover percentages, and geospatial metric records"]
    ]
    add_styled_table(headers_arch, rows_arch, [1.4, 1.4, 1.2, 2.4])

    add_h2("8.2 Dockerized Production Deployment on Render Cloud")
    add_p(
        "The entire platform is encapsulated into an optimized single-container Docker image deployed live on Render Cloud. The production container employs "
        "a multi-process supervisor executing Python Uvicorn on 127.0.0.1:8000 and Node.js on 0.0.0.0:10000. Real-time health monitoring endpoints (/health) "
        "ensure zero-downtime availability and graceful fallback during high traffic loads.",
        space_before=4, space_after=8
    )
    add_p(
        "Live Production URL: https://aeroseg-ai.onrender.com\nOfficial GitHub Repository: https://github.com/aniket821108/Aerial-LandCover-Segmentation-Mizoram",
        bold=True, italic=True, space_before=4, space_after=12
    )

    doc.add_page_break()

    # ==========================================
    # CHAPTER 9: CONCLUSION & FUTURE WORK
    # ==========================================
    add_h1("CHAPTER 9: CONCLUSION, SOCIETAL IMPACT & FUTURE WORK")
    add_h2("9.1 Summary of Contributions")
    add_p(
        "This undergraduate capstone project successfully tackled one of the most stubborn challenges in modern remote sensing: deep learning failure "
        "under extreme geospatial domain shift. The primary accomplishments include:",
        space_before=4, space_after=6
    )
    add_p("1. Formulated a Two-Tier Hybrid Architecture pairing Gemini 1.5 Vision AI guardrails with DeepLabV3+ segmentation to prevent corrupted inference.", space_after=4)
    add_p("2. Implemented Class-Balanced Self-Training (CBST), achieving a +4.52% net mIoU gain (+19.31% relative) and boosting rural road recovery by +11.27% without manual rural annotations.", space_after=4)
    add_p("3. Validated the methodology on 992 high-resolution validation GeoTIFF rasters, confirming 29.57% calibrated mIoU.", space_after=4)
    add_p("4. Built and deployed a live, fully functional cloud GIS platform providing real-time sub-meter hectare quantification for real-world governance.", space_after=10)

    add_h2("9.2 Practical Applications for Governance in Mizoram")
    add_p(
        "The operational utility of this framework directly addresses critical administrative priorities in Mizoram:",
        space_before=4, space_after=4
    )
    add_p("• Jhum Shifting Cultivation Monitoring: Quantifies the rapid transition between cleared forest slopes and active agricultural crops, assisting the Department of Agriculture in soil conservation and sustainable agro-forestry.", space_after=4)
    add_p("• Rural Road Infrastructure Planning: Enables automated mapping of remote cut-slope tracks and landslides across monsoon-affected hill terrain.", space_after=4)
    add_p("• Hydrological Basin Management: Accurately identifies riverbed narrowing and alluvial sediment accumulation across rural river basins.", space_after=10)

    add_h2("9.3 Future Research Directions")
    add_p(
        "Future enhancements will focus on integrating multi-temporal Sentinel-2 optical and Sentinel-1 Synthetic Aperture Radar (SAR) time-series to monitor "
        "vegetation regrowth through dense monsoon cloud cover. Additionally, integrating the Segment Anything Model (SAM) with prompt-based fine-tuning represents "
        "a compelling avenue for zero-shot geospatial generalization.",
        space_before=4, space_after=18
    )

    doc.add_page_break()

    # ==========================================
    # REFERENCES (IEEE STYLE)
    # ==========================================
    add_h1("REFERENCES")
    refs = [
        "[1] J. Wang, Z. Zheng, A. Ma, X. Lu, and Y. Zhong, \"LoveDA: A remote sensing land-cover dataset for domain adaptive semantic segmentation,\" in Proc. Neural Information Processing Systems (NeurIPS) Datasets and Benchmarks Track, 2021, pp. 1-14.",
        "[2] L.-C. Chen, Y. Zhu, G. Papandreou, F. Schroff, and H. Adam, \"Encoder-decoder with atrous separable convolution for semantic image segmentation,\" in Proc. European Conference on Computer Vision (ECCV), 2018, pp. 801-818.",
        "[3] L.-C. Chen, G. Papandreou, F. Schroff, and H. Adam, \"Rethinking atrous convolution for semantic image segmentation,\" arXiv preprint arXiv:1706.05587, 2017.",
        "[4] Y. Zou, Z. Yu, B. V. Kumar, and J. Wang, \"Unsupervised domain adaptation for semantic segmentation via class-balanced self-training,\" in Proc. European Conference on Computer Vision (ECCV), 2018, pp. 289-305.",
        "[5] Y. Zou, Z. Yu, X. Liu, B. V. Kumar, and J. Wang, \"Confidence regularized self-training for semantic segmentation,\" in Proc. IEEE/CVF International Conference on Computer Vision (ICCV), 2019, pp. 1982-1991.",
        "[6] K. He, X. Zhang, S. Ren, and J. Sun, \"Deep residual learning for image recognition,\" in Proc. IEEE Conference on Computer Vision and Pattern Recognition (CVPR), 2016, pp. 770-778.",
        "[7] J. Long, E. Shelhamer, and T. Darrell, \"Fully convolutional networks for semantic segmentation,\" in Proc. IEEE Conference on Computer Vision and Pattern Recognition (CVPR), 2015, pp. 3431-3440.",
        "[8] O. Ronneberger, P. Fischer, and T. Brox, \"U-Net: Convolutional networks for biomedical image segmentation,\" in Proc. Medical Image Computing and Computer-Assisted Intervention (MICCAI), 2015, pp. 234-241.",
        "[9] Y.-H. Tsai, W.-C. Hung, S. Schulter, K. Sohn, M.-H. Yang, and M. Chandraker, \"Learning to adapt structured output space for semantic segmentation,\" in Proc. IEEE Conference on Computer Vision and Pattern Recognition (CVPR), 2018, pp. 7472-7481.",
        "[10] Y. Ganin and V. Lempitsky, \"Unsupervised domain adaptation by backpropagation,\" in Proc. International Conference on Machine Learning (ICML), 2015, pp. 1180-1189.",
        "[11] M. Everingham, S. M. A. Eslami, L. Van Gool, C. K. I. Williams, J. Winn, and A. Zisserman, \"The PASCAL visual object classes challenge: A retrospective,\" International Journal of Computer Vision, vol. 111, no. 1, pp. 98-136, 2015.",
        "[12] Google DeepMind, \"Gemini: A family of highly capable multimodal models,\" arXiv preprint arXiv:2312.11805, 2023.",
        "[13] P. I. Team, \"Segmentation Models Pytorch,\" GitHub repository, https://github.com/qubvel/segmentation_models.pytorch, 2020.",
        "[14] F. Chollet, \"Xception: Deep learning with depthwise separable convolutions,\" in Proc. IEEE Conference on Computer Vision and Pattern Recognition (CVPR), 2017, pp. 1251-1258.",
        "[15] A. Paszke et al., \"PyTorch: An imperative style, high-performance deep learning library,\" in Advances in Neural Information Processing Systems (NeurIPS), 2019, pp. 8024-8035.",
        "[16] GDAL/OGR Contributors, \"GDAL/OGR Geospatial Data Abstraction software Library,\" Open Source Geospatial Foundation, 2023. [Online]. Available: https://gdal.org.",
        "[17] G. E. Woebbecke, G. E. Meyer, K. Von Bargen, and D. A. Mortensen, \"Color indices for weed identification under various soil, residue, and lighting conditions,\" Transactions of the ASAE, vol. 38, no. 1, pp. 259-269, 1995.",
        "[18] S. K. McFeeters, \"The use of the Normalized Difference Water Index (NDWI) in the delineation of open water features,\" International Journal of Remote Sensing, vol. 17, no. 7, pp. 1425-1432, 1996.",
        "[19] D. P. Kingma and J. Ba, \"Adam: A method for stochastic optimization,\" in Proc. International Conference on Learning Representations (ICLR), 2015.",
        "[20] I. Loshchilov and F. Hutter, \"Decoupled weight decay regularization,\" in Proc. International Conference on Learning Representations (ICLR), 2019.",
        "[21] H. Zhao, J. Shi, X. Qi, X. Wang, and J. Jia, \"Pyramid scene parsing network,\" in Proc. IEEE Conference on Computer Vision and Pattern Recognition (CVPR), 2017, pp. 2881-2890.",
        "[22] V. Badrinarayanan, A. Kendall, and R. Cipolla, \"SegNet: A deep convolutional encoder-decoder architecture for image segmentation,\" IEEE Transactions on Pattern Analysis and Machine Intelligence, vol. 39, no. 12, pp. 2481-2495, 2017.",
        "[23] A. Kirillov et al., \"Segment Anything,\" in Proc. IEEE/CVF International Conference on Computer Vision (ICCV), 2023, pp. 4015-4026.",
        "[24] Government of Mizoram, \"State Environment Report: Forest and Agricultural Land Use Dynamics in Mizoram,\" Department of Environment, Forests & Climate Change, Aizawl, 2022.",
        "[25] Indian Space Research Organisation (ISRO), \"National Land Use and Land Cover Mapping using Multi-Temporal Satellite Data,\" National Remote Sensing Centre (NRSC), Hyderabad, Tech. Rep., 2021."
    ]
    for r in refs:
        add_p(r, space_before=2, space_after=4, font_size=10)

    # Save DOCX
    doc.save(output_docx)
    print(f"[SUCCESS] Document generated successfully: {output_docx}")
    return output_docx

if __name__ == "__main__":
    create_report()
