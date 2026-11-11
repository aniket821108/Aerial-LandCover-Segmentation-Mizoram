import os
import sys
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image as RLImage, PageBreak, KeepTogether, HRFlowable
)
from reportlab.pdfgen import canvas

class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super(NumberedCanvas, self).__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_header_footer(num_pages)
            super(NumberedCanvas, self).showPage()
        super(NumberedCanvas, self).save()

    def draw_header_footer(self, page_count):
        if self._pageNumber > 1:
            self.saveState()
            self.setFont("Times-Roman", 8.5)
            self.setFillColor(colors.HexColor("#64748B"))
            # Header
            self.drawString(54, 750, "B.Tech Final Year Dissertation • Aerial Land-Use Segmentation (NIT Mizoram)")
            self.setStrokeColor(colors.HexColor("#CBD5E1"))
            self.setLineWidth(0.5)
            self.line(54, 744, 558, 744)
            
            # Footer
            self.line(54, 45, 558, 45)
            self.drawString(54, 34, "BT23CS028 • Aniket Kumar (Dept. of CSE, NIT Mizoram)")
            page_text = f"Page {self._pageNumber} of {page_count}"
            self.drawRightString(558, 34, page_text)
            self.restoreState()

def build_pdf():
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    results_dir = os.path.join(base_dir, "results")
    output_pdf = os.path.join(base_dir, "docs", "FINAL_ACADEMIC_PROJECT_REPORT.pdf")

    doc = SimpleDocTemplate(
        output_pdf,
        pagesize=letter,
        leftMargin=54,
        rightMargin=54,
        topMargin=54,
        bottomMargin=54
    )

    styles = getSampleStyleSheet()

    # Custom styles
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Normal'],
        fontName='Times-Bold',
        fontSize=20,
        leading=24,
        textColor=colors.HexColor("#0F172A"),
        alignment=1, # Center
        spaceAfter=10
    )
    subtitle_style = ParagraphStyle(
        'DocSubTitle',
        parent=styles['Normal'],
        fontName='Times-Italic',
        fontSize=12,
        leading=16,
        textColor=colors.HexColor("#334155"),
        alignment=1,
        spaceAfter=25
    )
    meta_style = ParagraphStyle(
        'DocMeta',
        parent=styles['Normal'],
        fontName='Times-Roman',
        fontSize=10.5,
        leading=15,
        textColor=colors.HexColor("#1E293B"),
        alignment=1,
        spaceAfter=15
    )
    h1_style = ParagraphStyle(
        'ChapterH1',
        parent=styles['Normal'],
        fontName='Times-Bold',
        fontSize=15,
        leading=19,
        textColor=colors.HexColor("#0F172A"),
        spaceBefore=14,
        spaceAfter=8,
        keepWithNext=True
    )
    h2_style = ParagraphStyle(
        'ChapterH2',
        parent=styles['Normal'],
        fontName='Times-Bold',
        fontSize=12,
        leading=16,
        textColor=colors.HexColor("#1E3A8A"),
        spaceBefore=10,
        spaceAfter=5,
        keepWithNext=True
    )
    body_style = ParagraphStyle(
        'DocBody',
        parent=styles['Normal'],
        fontName='Times-Roman',
        fontSize=10,
        leading=14.5,
        textColor=colors.HexColor("#1E293B"),
        spaceAfter=6,
        alignment=4 # Justified
    )
    callout_style = ParagraphStyle(
        'CalloutText',
        parent=styles['Normal'],
        fontName='Times-Roman',
        fontSize=9.5,
        leading=13.5,
        textColor=colors.HexColor("#0F172A")
    )
    caption_style = ParagraphStyle(
        'FigCaption',
        parent=styles['Normal'],
        fontName='Times-Italic',
        fontSize=8.5,
        leading=11.5,
        textColor=colors.HexColor("#475569"),
        alignment=1, # Center
        spaceBefore=4,
        spaceAfter=10
    )

    story = []

    def p(text, style=body_style):
        return Paragraph(text, style)

    def callout(title, text):
        data = [[
            Paragraph(f"<b><font color='#0284C7'>{title}:</font></b> {text}", callout_style)
        ]]
        t = Table(data, colWidths=[500])
        t.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#F1F5F9")),
            ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#CBD5E1")),
            ('PADDING', (0,0), (-1,-1), 8),
            ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ]))
        return t

    def styled_table(headers, rows, col_widths=None):
        header_pars = [Paragraph(f"<b><font color='white'>{h}</font></b>", ParagraphStyle('TH', fontName='Times-Bold', fontSize=8.5, leading=10.5, alignment=1)) for h in headers]
        table_data = [header_pars]
        for row in rows:
            row_pars = []
            for idx, val in enumerate(row):
                align = 0 if idx == 0 else 1
                weight = 'Times-Bold' if idx == 0 else 'Times-Roman'
                color = '#0F172A' if idx == 0 else '#334155'
                par = Paragraph(f"<font color='{color}'>{val}</font>", ParagraphStyle('TD', fontName=weight, fontSize=8, leading=10.5, alignment=align))
                row_pars.append(par)
            table_data.append(row_pars)

        t = Table(table_data, colWidths=col_widths)
        t_style = [
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#1E293B")),
            ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#E2E8F0")),
            ('TOPPADDING', (0, 0), (-1, -1), 4),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ]
        for i in range(1, len(table_data)):
            bg = colors.HexColor("#F8FAFC") if i % 2 == 1 else colors.white
            t_style.append(('BACKGROUND', (0, i), (-1, i), bg))
        t.setStyle(TableStyle(t_style))
        return t

    def fig(img_name, caption_text, width=420, height=210):
        img_path = os.path.join(results_dir, img_name)
        elements = []
        if os.path.exists(img_path):
            img = RLImage(img_path, width=width, height=height)
            elements.append(Spacer(1, 6))
            elements.append(img)
            elements.append(Paragraph(caption_text, caption_style))
            elements.append(Spacer(1, 6))
        return elements

    # ==========================
    # 1. COVER PAGE
    # ==========================
    story.append(Spacer(1, 30))
    story.append(Paragraph("A DISSERTATION ON", ParagraphStyle('PreTitle', fontName='Times-Bold', fontSize=11, leading=14, textColor=colors.HexColor("#64748B"), alignment=1)))
    story.append(Spacer(1, 10))
    story.append(Paragraph("AERIAL IMAGE SEGMENTATION FOR LAND USE CLASSIFICATION", title_style))
    story.append(Paragraph("A Two-Tier Multimodal Vision AI Guardrail and Class-Balanced Self-Training Domain Adaptation Framework for Rugged Rural Terrain", subtitle_style))
    story.append(Spacer(1, 15))

    story.append(Paragraph("Submitted in partial fulfillment of the requirements for the award of the degree of<br/><b>BACHELOR OF TECHNOLOGY</b><br/>IN<br/><b>COMPUTER SCIENCE AND ENGINEERING</b>", meta_style))
    story.append(Spacer(1, 35))

    # Two column table for student & supervisor
    info_data = [
        [
            Paragraph("<b>SUBMITTED BY:</b><br/><b>ANIKET KUMAR</b><br/>Enrollment No: BT23CS028<br/>Department of CSE", ParagraphStyle('L', fontName='Times-Roman', fontSize=10, leading=14, alignment=0)),
            Paragraph("<b>UNDER THE GUIDANCE OF:</b><br/><b>Dr. TANMAY KUMAR BEHERA</b><br/>Assistant Professor<br/>Department of CSE", ParagraphStyle('R', fontName='Times-Roman', fontSize=10, leading=14, alignment=2))
        ]
    ]
    t_info = Table(info_data, colWidths=[250, 250])
    t_info.setStyle(TableStyle([('VALIGN', (0,0), (-1,-1), 'TOP')]))
    story.append(t_info)
    story.append(Spacer(1, 50))

    story.append(Paragraph("<b>DEPARTMENT OF COMPUTER SCIENCE AND ENGINEERING<br/>NATIONAL INSTITUTE OF TECHNOLOGY MIZORAM<br/>AIZAWL, MIZORAM – 796012, INDIA</b>", ParagraphStyle('Univ', fontName='Times-Bold', fontSize=10.5, leading=15, textColor=colors.HexColor("#0F172A"), alignment=1)))
    story.append(PageBreak())

    # ==========================
    # 2. CERTIFICATE
    # ==========================
    story.append(Paragraph("<b>NATIONAL INSTITUTE OF TECHNOLOGY MIZORAM</b><br/><font size=9 color='#475569'>Department of Computer Science and Engineering • Aizawl, Mizoram – 796012, India</font>", ParagraphStyle('C1', fontName='Times-Bold', fontSize=12, leading=16, alignment=1)))
    story.append(Spacer(1, 15))
    story.append(Paragraph("CERTIFICATE OF RECOMMENDATION", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#1E3A8A"), spaceBefore=2, spaceAfter=15))

    cert_text = (
        "This is to certify that the dissertation entitled <b>\"Aerial Image Segmentation for Land Use Classification: "
        "A Two-Tier Multimodal Vision AI Guardrail and Class-Balanced Self-Training Domain Adaptation Framework for Rugged Rural Terrain\"</b>, "
        "submitted by <b>ANIKET KUMAR (Enrollment No. BT23CS028)</b> in partial fulfillment of the requirements for the award of the degree of "
        "<b>Bachelor of Technology in Computer Science and Engineering</b> at the National Institute of Technology Mizoram, is an authentic record of "
        "bonafide research and technical work carried out under my supervision and guidance.<br/><br/>"
        "To the best of my knowledge, the matter embodied in this dissertation has not been submitted in part or full to any other University or "
        "Institute for the award of any degree, diploma, or academic distinction."
    )
    story.append(Paragraph(cert_text, body_style))
    story.append(Spacer(1, 55))

    sig_data = [
        [
            Paragraph("______________________________<br/><b>Dr. Tanmay Kumar Behera</b><br/>Supervisor / Assistant Professor<br/>Department of CSE, NIT Mizoram", ParagraphStyle('SL', fontName='Times-Roman', fontSize=9.5, leading=13)),
            Paragraph("______________________________<br/><b>Head of the Department</b><br/>Department of CSE<br/>NIT Mizoram", ParagraphStyle('SR', fontName='Times-Roman', fontSize=9.5, leading=13, alignment=2))
        ]
    ]
    t_sig = Table(sig_data, colWidths=[250, 250])
    story.append(t_sig)
    story.append(Spacer(1, 35))

    story.append(Paragraph("______________________________<br/><b>External Examiner</b><br/>(Board of Examiners)", ParagraphStyle('SE', fontName='Times-Roman', fontSize=9.5, leading=13, alignment=1)))
    story.append(PageBreak())

    # ==========================
    # 3. DECLARATION & ACKNOWLEDGMENTS
    # ==========================
    story.append(Paragraph("CANDIDATE'S DECLARATION", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#1E3A8A"), spaceBefore=2, spaceAfter=12))
    dec_text = (
        "I hereby declare that the work presented in this final-year B.Tech capstone project report entitled <b>\"Aerial Image Segmentation for Land Use "
        "Classification\"</b> is an authentic record of my own investigation carried out under the supervision of Dr. Tanmay Kumar Behera, Assistant Professor, "
        "Department of Computer Science and Engineering, National Institute of Technology Mizoram.<br/><br/>"
        "I have adhered to all academic ethics and honesty standards. No portion of this technical report or codebase has been plagiarized, and all external "
        "literature, benchmarks, algorithms, and software libraries (including the LoveDA benchmark, DeepLabV3+ architecture, PyTorch, GDAL, "
        "and Google Gemini APIs) have been appropriately referenced."
    )
    story.append(Paragraph(dec_text, body_style))
    story.append(Spacer(1, 15))
    story.append(Paragraph("<b>Aniket Kumar</b><br/>Enrollment No. BT23CS028<br/>B.Tech (Final Year), CSE<br/>NIT Mizoram", ParagraphStyle('SigD', fontName='Times-Roman', fontSize=9.5, leading=13, alignment=2)))
    story.append(Spacer(1, 25))

    story.append(Paragraph("ACKNOWLEDGMENTS", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#1E3A8A"), spaceBefore=2, spaceAfter=12))
    ack_text = (
        "I express my deepest gratitude to my project supervisor, <b>Dr. Tanmay Kumar Behera</b>, Assistant Professor, Department of Computer Science and "
        "Engineering, National Institute of Technology Mizoram, for his inspiring guidance, critical feedback, and constant encouragement throughout "
        "the conceptualization, mathematical formulation, and experimental execution of this research.<br/><br/>"
        "I extend my sincere thanks to the Head of the Department and all faculty members of the Department of Computer Science and Engineering for "
        "providing the computational resources and intellectual environment necessary to complete this project.<br/><br/>"
        "Finally, I am profoundly grateful to my parents and peers for their unwavering patience, support, and motivation."
    )
    story.append(Paragraph(ack_text, body_style))
    story.append(PageBreak())

    # ==========================
    # 4. ABSTRACT
    # ==========================
    story.append(Paragraph("ABSTRACT", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#1E3A8A"), spaceBefore=2, spaceAfter=12))
    abs_p1 = (
        "High-resolution aerial and satellite remote sensing enables automated land-cover mapping essential for environmental governance, urban planning, "
        "disaster resilience, and agricultural monitoring. However, contemporary deep convolutional semantic segmentation networks suffer catastrophic "
        "performance degradation when deployed across heterogeneous geospatial domains due to significant domain shift. In particular, deep models trained "
        "on structured, high-density urban aerial imagery fail drastically when applied to complex rural and montane environments—such as the rugged ridgelines, "
        "shifting Jhum cultivation plots, and unpaved corridors characteristic of Mizoram and Northeast India."
    )
    abs_p2 = (
        "In this dissertation, we present a robust, production-grade end-to-end framework that resolves this challenge through a novel two-tier architecture "
        "combining multimodal vision foundation intelligence with unsupervised domain adaptation. In Tier 1, an enterprise-grade Multimodal Vision AI "
        "(Google Gemini 1.5 Vision) serves as an operational gatekeeper and semantic guardrail, inspecting incoming orthophotos to verify orthogonal perspective "
        "validity, flag terrestrial/non-aerial corruptions, and identify macro-terrain contexts. In Tier 2, high-altitude aerial scenes are segmented using a "
        "DeepLabV3+ architecture with a ResNet-50 feature backbone and Atrous Spatial Pyramid Pooling (ASPP)."
    )
    abs_p3 = (
        "To overcome the severe domain gap without requiring costly manual pixel annotations on rural terrain, we implement Class-Balanced Self-Training (CBST). "
        "CBST adaptively calculates class-specific confidence thresholds (&lambda;<sub>c</sub>) to extract high-confidence pseudo-labels from unlabeled target imagery, "
        "effectively preventing majority classes from dominating gradient updates. Experimental benchmarking on the rigorous LoveDA Land-Cover dataset reveals "
        "that direct cross-domain transfer experiences a steep 15.55% mIoU domain penalty (dropping from 38.93% on urban source data to 23.39% on rural target data). "
        "Following CBST domain adaptation, our model achieves <b>27.90% mIoU</b>, delivering a net improvement of <b>+4.52% mIoU (+19.31% relative gain)</b>. Crucially, "
        "sparse and critical rural classes experience dramatic recoveries: <b>Road IoU surges by +11.27% (from 20.03% to 31.30%)</b>, Water IoU increases by +7.95% "
        "(from 38.21% to 46.15%), and Agriculture increases by +5.88% (from 42.31% to 48.19%). Validation across 992 high-resolution GeoTIFF rasters confirms "
        "29.57% calibrated raster mIoU."
    )
    abs_p4 = (
        "Furthermore, we bridge machine learning research and practical GIS governance by developing a full-stack, cloud-deployed web portal "
        "(React 19, Node.js/Express, Python FastAPI, MongoDB Atlas, Dockerized and hosted on Render) that performs real-time pixel-to-hectare land-use quantification "
        "using sub-meter Ground Sampling Distance (GSD) calculus."
    )
    story.append(p(abs_p1))
    story.append(p(abs_p2))
    story.append(p(abs_p3))
    story.append(p(abs_p4))
    story.append(Spacer(1, 6))
    story.append(Paragraph("<b>Keywords:</b> <i>Aerial Image Segmentation, DeepLabV3+, Unsupervised Domain Adaptation, Class-Balanced Self-Training (CBST), Geospatial Analytics, Multimodal Vision AI Guardrail, LoveDA Benchmark, Mizoram Remote Sensing.</i>", ParagraphStyle('KW', fontName='Times-Roman', fontSize=9, leading=13, textColor=colors.HexColor("#1E3A8A"))))
    story.append(PageBreak())

    # ==========================
    # CHAPTER 1: INTRODUCTION
    # ==========================
    story.append(Paragraph("CHAPTER 1: INTRODUCTION & PROBLEM DEFINITION", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#1E3A8A"), spaceBefore=2, spaceAfter=10))

    story.append(Paragraph("1.1 Background and Significance of Aerial Remote Sensing", h2_style))
    story.append(p(
        "Earth observation and aerial remote sensing have undergone a transformative paradigm shift with the rapid convergence of high-resolution "
        "spaceborne sensors, Unmanned Aerial Vehicles (UAVs), and deep convolutional neural networks. Modern optical sensors acquire high-resolution "
        "orthophotos with Ground Sampling Distances (GSD) beneath 0.5 meters per pixel, uncovering fine-grained geometric details ranging from individual "
        "building rooflines to narrow transport corridors and minor riparian waterways. Extracting accurate, pixel-level land-use and land-cover (LULC) maps "
        "from these complex aerial images is indispensable for urban planning, hydrological basin modeling, automated disaster damage assessment, and "
        "forest conservation."
    ))

    story.append(Paragraph("1.2 Topographic Challenges of Mizoram & Northeast India", h2_style))
    story.append(p(
        "While computer vision models achieve state-of-the-art segmentation benchmark scores on standardized metropolitan datasets (e.g. European and East Asian "
        "megacities), deploying these models in rural, montane geographies introduces severe domain failure. The state of Mizoram, nestled in the southern "
        "reach of Northeast India, exemplifies these extreme challenges. Characterized by parallel north-south oriented hill ridges, steep valley gorges, "
        "dense subtropical evergreen forests, and pervasive 'Jhum' (slash-and-burn shifting cultivation) agro-forestry cycles, Mizoram's terrain differs "
        "fundamentally from rectilinear urban environments."
    ))
    story.append(p(
        "In rural Mizoram, transport infrastructure consists primarily of sinuous, unpaved or cut-slope roadways that visually blend into flanking barren "
        "earth or scrub vegetation. Settlements comprise scattered clusters of tin-roofed and bamboo dwellings clinging to ridge spurs rather than uniform "
        "concrete street grids. Furthermore, agricultural plots in Mizoram undergo rapid seasonal transitions from cleared barren slopes to active green crops, "
        "producing intense intra-class spectral variance."
    ))

    story.append(Paragraph("1.3 The Domain Shift Problem in Remote Sensing", h2_style))
    story.append(p(
        "When a deep semantic segmentation model trained on annotated urban orthophotos is directly evaluated on target rural imagery, a catastrophic drop in "
        "mean Intersection-over-Union (mIoU) occurs. This phenomenon—termed domain shift—is driven by discrepancies in both marginal image distributions "
        "P(X) and conditional distributions P(Y|X)."
    ))
    story.append(callout(
        "THE DOMAIN GAP PENALTY",
        "Evaluating an Urban-trained DeepLabV3+ model directly on Rural aerial imagery resulted in a catastrophic 15.55% mIoU drop (from 38.93% down to 23.39%). "
        "Road segmentation collapsed by 24.87% and Forest segmentation plummeted by 23.83%, rendering the direct transfer model operationally unusable."
    ))

    story.append(Paragraph("1.4 Project Objectives and Key Contributions", h2_style))
    story.append(p("• <b>Two-Tier Hybrid Architecture:</b> Multimodal Gemini 1.5 Vision guardrail + deep segmentation backbone to eliminate corrupted inputs."))
    story.append(p("• <b>DeepLabV3+ & ASPP Optimization:</b> Capture multi-scale context across complex rural land forms."))
    story.append(p("• <b>Class-Balanced Self-Training (CBST):</b> Unsupervised adaptation recovering sparse rural classes without manual annotations."))
    story.append(p("• <b>Large-Scale GeoTIFF Validation:</b> Comprehensive evaluation over 992 high-resolution validation GeoTIFF rasters."))
    story.append(p("• <b>Live Cloud GIS Platform:</b> Dockerized MERN + FastAPI application delivering real-time sub-meter hectare quantification on Render."))
    story.append(PageBreak())

    # ==========================
    # CHAPTER 2: LITERATURE REVIEW
    # ==========================
    story.append(Paragraph("CHAPTER 2: LITERATURE REVIEW & RELATED WORK", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#1E3A8A"), spaceBefore=2, spaceAfter=10))

    story.append(Paragraph("2.1 Semantic Segmentation in Remote Sensing", h2_style))
    story.append(p(
        "Semantic segmentation assigns a discrete categorical label to each individual pixel. Early remote sensing pipelines relied on manual feature "
        "engineering, such as spectral angle mappers, Support Vector Machines (SVM), and Random Forests operating on normalized indices (NDVI, NDWI). "
        "The advent of deep Convolutional Neural Networks (CNNs) revolutionized the field. Long et al. (2015) introduced Fully Convolutional Networks (FCN), "
        "and Ronneberger et al. (2015) advanced biomedical and satellite segmentation with U-Net, introducing symmetric contracting and expanding paths bridged "
        "by skip connections."
    ))

    story.append(Paragraph("2.2 DeepLabV3+ and Atrous Spatial Pyramid Pooling (ASPP)", h2_style))
    story.append(p(
        "Standard convolutional downsampling inherently degrades spatial feature resolution. Chen et al. (2017, 2018) addressed this trade-off through atrous "
        "(dilated) convolutions. By inserting holes into convolution kernels, atrous convolutions expand the effective receptive field without increasing parameter "
        "count or reducing spatial grid resolution. DeepLabV3+ introduces ASPP, applying multiple parallel atrous convolutions with dilations r &isin; {6, 12, 18} "
        "alongside global average pooling, capturing multi-scale context ranging from broad forest canopies to narrow roads."
    ))

    story.append(Paragraph("2.3 Unsupervised Domain Adaptation (UDA) & CBST", h2_style))
    story.append(p(
        "Unsupervised Domain Adaptation (UDA) addresses scenarios where labeled source data is abundant, but target data lacks ground-truth annotations. "
        "While adversarial alignment (AdaptSegNet) suffers from training instability and mode collapse on remote sensing data, self-training (Zou et al., 2018) "
        "iteratively generates pseudo-labels on target imagery. Class-Balanced Self-Training (CBST) dynamically optimizes class-specific thresholds &lambda;<sub>c</sub>, "
        "preventing dominant categories from monopolizing supervision and starving minority categories (Roads, Barren)."
    ))

    headers_lit = ["Architecture / Framework", "Core Mechanism", "Primary Advantage", "Observed Limitation in Remote Sensing"]
    rows_lit = [
        ["FCN-8s (Long et al.)", "Skip-layer feature combination", "End-to-end pixel classification", "Coarse boundary predictions; lacks multi-scale context"],
        ["U-Net (Ronneberger et al.)", "Symmetric encoder-decoder + skips", "Precise edge and shape recovery", "Over-reliant on local cues; prone to large-scale context errors"],
        ["AdaptSegNet (Tsai et al.)", "Adversarial output space alignment", "Domain-invariant representations", "High training instability; fails on skewed class distributions"],
        ["DeepLabV3+ (Chen et al.)", "ASPP + Dilated Convolutions", "Superior multi-scale feature capture", "Severe performance drop under cross-domain distribution shifts"],
        ["Our Proposed Framework", "Two-Tier Gemini Guardrail + CBST", "Robust gatekeeper + class-balanced UDA", "Requires multi-stage iterative retraining"]
    ]
    story.append(Spacer(1, 4))
    story.append(styled_table(headers_lit, rows_lit, [110, 130, 130, 130]))
    story.append(PageBreak())

    # ==========================
    # CHAPTER 3: DATASET ARCHITECTURE
    # ==========================
    story.append(Paragraph("CHAPTER 3: DATASET ARCHITECTURE & GEOSPATIAL METHODOLOGY", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#1E3A8A"), spaceBefore=2, spaceAfter=10))

    story.append(Paragraph("3.1 The LoveDA Remote Sensing Benchmark", h2_style))
    story.append(p(
        "To rigorously evaluate domain shift under real-world conditions, we employ the Land-Cover Domain Adaptive (LoveDA) benchmark dataset (Wang et al., 2021). "
        "Acquired across Nanjing, Changzhou, and Wuhan using high-altitude aerial platforms, LoveDA comprises 5,987 total high-resolution image patches "
        "(1024 &times; 1024 pixels at 0.3 m/pixel GSD). LoveDA features two clearly bifurcated domains: Urban (Source, high-density metropolitan infrastructure) "
        "and Rural (Target, complex rural basins, unpaved roads, terraced farmlands)."
    ))

    story.append(Paragraph("3.2 Seven-Class Land-Cover Taxonomy", h2_style))
    headers_tax = ["ID", "Class Name", "Hex Color", "RGB Palette", "Geospatial Definition in Rural Mizoram Context"]
    rows_tax = [
        ["0", "Background", "#2A2A2A", "[42, 42, 42]", "Unclassified regions, clouds, sensor shadows, out-of-boundary pixels"],
        ["1", "Building", "#EF4444", "[239, 68, 68]", "Residential homes, agricultural storehouses, tin-roofed dwellings"],
        ["2", "Road", "#EAB308", "[234, 179, 8]", "Paved highways, cut-slope hillside corridors, unpaved village tracks"],
        ["3", "Water", "#3B82F6", "[59, 130, 246]", "Rivers, mountain streams, irrigation retention ponds, alluvial channels"],
        ["4", "Barren", "#A855F7", "[168, 85, 247]", "Exposed rock spurs, landslide scars, cleared soil, excavation zones"],
        ["5", "Forest", "#22C55E", "[34, 197, 94]", "Dense subtropical evergreen forest, bamboo groves, protected hill canopy"],
        ["6", "Agriculture", "#F97316", "[249, 115, 22]", "Terraced hill crops, valley rice paddies, active Jhum cultivation parcels"]
    ]
    story.append(styled_table(headers_tax, rows_tax, [30, 80, 65, 85, 240]))
    story.append(Spacer(1, 8))

    story.append(Paragraph("3.3 Ground Sampling Distance & Metric Hectare Calculus", h2_style))
    story.append(p(
        "In high-resolution remote sensing, each pixel represents a calibrated physical ground area determined by the Ground Sampling Distance (GSD):<br/>"
        "&bull; Pixel Area (m&sup2;) = GSD &times; GSD<br/>"
        "&bull; Class Area (Hectares) = (Pixel Count &times; GSD&sup2;) / 10,000<br/>"
        "For standard LoveDA orthophotos (1024 &times; 1024 pixels at GSD = 0.3 m/pixel), each pixel covers exactly 0.09 m&sup2;, yielding a total tile ground "
        "footprint of 94,371.84 m&sup2; (9.4372 Hectares)."
    ))
    story.append(PageBreak())

    # ==========================
    # CHAPTER 4: METHODOLOGY & ARCHITECTURE
    # ==========================
    story.append(Paragraph("CHAPTER 4: METHODOLOGY & DEEP LEARNING ARCHITECTURE", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#1E3A8A"), spaceBefore=2, spaceAfter=10))

    story.append(Paragraph("4.1 Two-Tier System Architecture Overview", h2_style))
    story.append(p(
        "Conventional deep segmentation pipelines directly ingest raw uploaded imagery without verifying operational suitability. Our framework introduces a Two-Tier Architecture:<br/>"
        "&bull; <b>Tier 1 (Domain Gatekeeper):</b> Multimodal Gemini 1.5 Vision AI verifies orthogonal orientation and valid aerial perspective.<br/>"
        "&bull; <b>Tier 2 (Deep Segmentation):</b> DeepLabV3+ with ResNet-50 and ASPP performs pixel-level semantic segmentation and GDAL metric quantification."
    ))

    story.extend(fig("side_by_side_comparison.png", "Figure 4.1: End-to-End Visual Pipeline: Input Orthophoto, Ground Truth Annotation, and Final Domain-Adapted Prediction.", width=450, height=200))

    story.append(Paragraph("4.2 DeepLabV3+ with ResNet-50 Feature Backbone", h2_style))
    story.append(p(
        "The segmentation core implements DeepLabV3+ utilizing a ResNet-50 backbone initialized with ImageNet pre-trained weights. ResNet-50 comprises 53 "
        "convolutional layers. In stages 3 and 4, standard downsampling strides are modified to atrous convolutions with output stride OS = 16, preserving spatial "
        "coordinate fidelity. The ASPP module applies 5 parallel branches (one 1&times;1 conv, three 3&times;3 atrous convs with rates r &isin; {6, 12, 18}, and image pooling), "
        "fusing multi-scale context before decoding with low-level features."
    ))
    story.append(PageBreak())

    # ==========================
    # CHAPTER 5: UNSUPERVISED DOMAIN ADAPTATION VIA CBST
    # ==========================
    story.append(Paragraph("CHAPTER 5: UNSUPERVISED DOMAIN ADAPTATION VIA CBST", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#1E3A8A"), spaceBefore=2, spaceAfter=10))

    story.append(Paragraph("5.1 Mathematical Formulation of Class-Balanced Self-Training", h2_style))
    story.append(p(
        "In self-training, the model generates soft probability distributions P<sub>c</sub>(u, v) = softmax(z<sub>c</sub>(u, v)) on unlabeled target images. "
        "CBST defines an optimization objective over model parameters w and latent pseudo-labels &ycirc;:<br/>"
        "<b>min<sub>w, &ycirc;</sub> L(w, &ycirc;) = L<sub>s</sub>(w) - &sum;<sub>j</sub> &sum;<sub>u,v</sub> &sum;<sub>c</sub> &ycirc;<sub>j,c</sub>(u, v) log( P<sub>c</sub>(u, v | x<sub>j</sub><sup>t</sup>; w) / &lambda;<sub>c</sub> )</b>"
    ))

    story.append(Paragraph("5.2 Class-Specific Threshold Selection (&lambda;<sub>c</sub>)", h2_style))
    story.append(p(
        "Rather than imposing a single global confidence cutoff, CBST adaptively determines class-specific thresholds &lambda;<sub>c</sub>. For each class c, "
        "the system ranks all predicted probabilities across the target corpus and sets &lambda;<sub>c</sub> such that top proportion p<sub>c</sub> of candidate pixels are selected:<br/>"
        "<b>&lambda;<sub>c</sub> = Percentile( { P<sub>c</sub>(u, v | x<sub>j</sub><sup>t</sup>) }, 1 - p<sub>c</sub> )</b><br/>"
        "Hard pseudo-labels are assigned to the class maximizing the normalized confidence ratio. This guarantees that minority categories (Roads, Barren) "
        "receive substantial pseudo-label representation, preventing gradient starvation and model collapse."
    ))
    story.append(PageBreak())

    # ==========================
    # CHAPTER 6: EXPERIMENTAL SETUP
    # ==========================
    story.append(Paragraph("CHAPTER 6: EXPERIMENTAL SETUP & TRAINING METHODOLOGY", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#1E3A8A"), spaceBefore=2, spaceAfter=10))

    story.append(Paragraph("6.1 Hardware and Compute Infrastructure", h2_style))
    story.append(p(
        "Model training, adaptation loops, and ablation evaluations were conducted using PyTorch 2.0 with CUDA 11.8 on NVIDIA Tesla T4 GPUs (16 GB VRAM) "
        "under Google Colab Pro infrastructure, augmented with high-RAM system nodes (51 GB RAM). Standalone microservice deployment was implemented "
        "using Docker on Render Cloud nodes running Python 3.11 and Node.js 20."
    ))

    story.append(Paragraph("6.2 Training Protocols and Hyperparameter Configuration", h2_style))
    headers_hp = ["Hyperparameter Name", "Baseline Source Training", "CBST Adaptation Stage", "Justification & Impact"]
    rows_hp = [
        ["Optimizer", "AdamW", "AdamW", "Decoupled weight decay prevents overfitting on high-frequency noise"],
        ["Initial Learning Rate", "1.0 &times; 10⁻⁴", "2.5 &times; 10⁻⁵", "Lower learning rate prevents catastrophic forgetting of source features"],
        ["LR Decay Policy", "Polynomial (power=0.9)", "Polynomial (power=0.9)", "Smooth convergence towards global minima"],
        ["Batch Size", "8 patches", "4 patches (dual pass)", "Maximizes GPU VRAM utilization for 1024&times;1024 images"],
        ["Input Resolution", "1024 &times; 1024 pixels", "1024 &times; 1024 pixels", "Preserves native LoveDA sub-meter GSD spatial resolution"],
        ["Data Augmentations", "H-Flip, V-Flip, ScaleRotate", "H-Flip, V-Flip, ColorJitter", "Enforces rotational and illumination invariance in montane terrain"],
        ["CBST Target Ratio (p_c)", "N/A", "0.20 &rarr; 0.35 (progressive)", "Prevents early pseudo-label drift while scaling supervision"]
    ]
    story.append(styled_table(headers_hp, rows_hp, [110, 110, 110, 170]))
    story.append(PageBreak())

    # ==========================
    # CHAPTER 7: RESULTS & DISCUSSION
    # ==========================
    story.append(Paragraph("CHAPTER 7: RESULTS, ABLATION STUDIES & DISCUSSION", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#1E3A8A"), spaceBefore=2, spaceAfter=10))

    story.append(Paragraph("7.1 Domain Shift Discrepancy (Urban vs Rural)", h2_style))
    headers_gap = ["Land-Cover Class", "Source Domain IoU (Urban)", "Direct Transfer IoU (Rural)", "Absolute Domain Drop (&Delta;)", "Relative Drop (%)"]
    rows_gap = [
        ["Building", "43.54%", "22.96%", "-20.58%", "-47.27%"],
        ["Road", "44.90%", "20.03%", "-24.87%", "-55.39%"],
        ["Water", "55.57%", "38.21%", "-17.36%", "-31.24%"],
        ["Barren", "4.84%", "2.15%", "-2.69%", "-55.58%"],
        ["Forest", "38.48%", "14.65%", "-23.83%", "-61.93%"],
        ["Agriculture", "46.27%", "42.31%", "-3.96%", "-8.56%"],
        ["OVERALL mIoU", "38.93%", "23.39%", "-15.55%", "-39.94%"]
    ]
    story.append(styled_table(headers_gap, rows_gap, [100, 100, 100, 100, 100]))
    story.append(Spacer(1, 6))

    story.append(Paragraph("7.2 CBST Domain Adaptation Gains", h2_style))
    headers_cbst = ["Land-Cover Class", "Baseline Rural IoU", "CBST Adapted Rural IoU", "Net Absolute Gain (&Delta;)", "Relative Improvement (%)"]
    rows_cbst = [
        ["Building", "22.96%", "22.40%", "-0.56%", "-2.44%"],
        ["Road", "20.03%", "31.30%", "+11.27%", "+56.27% (SURGE)"],
        ["Water", "38.21%", "46.15%", "+7.95%", "+20.80%"],
        ["Barren", "2.15%", "1.39%", "-0.76%", "-35.35%"],
        ["Forest", "14.65%", "17.97%", "+3.32%", "+22.66%"],
        ["Agriculture", "42.31%", "48.19%", "+5.88%", "+13.90%"],
        ["RURAL mIoU", "23.39%", "27.90%", "+4.52%", "+19.31% GAIN"]
    ]
    story.append(styled_table(headers_cbst, rows_cbst, [100, 100, 100, 100, 100]))
    story.append(Spacer(1, 6))

    story.append(callout(
        "CRITICAL BREAKTHROUGH ON TRANSPORT CORRIDORS",
        "CBST adaptation achieved a dramatic breakthrough on Road segmentation, boosting IoU from 20.03% to 31.30%—a remarkable +56.27% relative surge. "
        "In rural and mountainous terrains like Mizoram, unpaved secondary corridors are routinely misclassified as barren soil by standard models. "
        "Class-balanced thresholding forced the model to extract high-confidence road segments, resolving road continuity across valley corridors."
    ))

    story.extend(fig("cbst_comparison_bar.png", "Figure 7.1: Quantitative Comparison: Baseline Direct Transfer vs. CBST Domain-Adapted Model Across All Classes.", width=450, height=200))
    story.extend(fig("slide_segmentation_gallery_16x9.png", "Figure 7.2: Qualitative Benchmark Gallery Across Rural Test Scenes: Input RGB, Color-Coded Prediction, and Ground Truth.", width=450, height=210))
    story.append(PageBreak())

    # ==========================
    # CHAPTER 8: FULL-STACK APPLICATION
    # ==========================
    story.append(Paragraph("CHAPTER 8: FULL-STACK CLOUD APPLICATION & PRODUCTION DEPLOYMENT", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#1E3A8A"), spaceBefore=2, spaceAfter=10))

    story.append(Paragraph("8.1 System Architecture Overview", h2_style))
    story.append(p(
        "To deliver actionable utility to GIS officers and municipal engineers in Mizoram, we deployed a complete full-stack web application. "
        "The platform combines a React 19 Single-Page Application, an Express.js API gateway, a Python FastAPI microservice, and MongoDB Atlas."
    ))

    headers_arch = ["Component Layer", "Technology Stack", "Port & Runtime", "Functional Responsibilities"]
    rows_arch = [
        ["Client (Frontend)", "React 19, Vite, Tailwind CSS, Lucide Icons", "Served via Express static asset engine", "Interactive visual split comparison, real-time GSD slider, interactive donut charts, history drawer"],
        ["API Gateway (Backend)", "Node.js 20, Express.js, Multer, Mongoose", "Port 10000 (Render external edge)", "Request orchestration, Tier-1 Gemini Vision AI invocation, MongoDB history persistence, rate limiting"],
        ["ML Microservice", "Python 3.11, FastAPI, PyTorch, PIL, NumPy", "Port 8000 (Internal loopback)", "DeepLabV3+ ResNet-50 inference, spectral proxy classifier, single-band GeoTIFF raster encoding"],
        ["Database Layer", "MongoDB Atlas (M0 Shared Cluster)", "Cloud Hosted (yi4ir.mongodb.net)", "Persistent audit trail, scan telemetry, land-cover percentages, and geospatial metric records"]
    ]
    story.append(styled_table(headers_arch, rows_arch, [100, 110, 110, 180]))
    story.append(Spacer(1, 10))

    story.append(p("<b>Live Production Deployment:</b> https://aeroseg-ai.onrender.com<br/><b>Official GitHub Repository:</b> https://github.com/aniket821108/Aerial-LandCover-Segmentation-Mizoram", ParagraphStyle('LiveURL', fontName='Times-Bold', fontSize=9.5, leading=14, textColor=colors.HexColor("#0284C7"))))
    story.append(PageBreak())

    # ==========================
    # CHAPTER 9: CONCLUSION & FUTURE WORK
    # ==========================
    story.append(Paragraph("CHAPTER 9: CONCLUSION, SOCIETAL IMPACT & FUTURE WORK", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#1E3A8A"), spaceBefore=2, spaceAfter=10))

    story.append(Paragraph("9.1 Summary of Contributions", h2_style))
    story.append(p("1. Formulated a Two-Tier Hybrid Architecture pairing Gemini 1.5 Vision AI guardrails with DeepLabV3+ segmentation."))
    story.append(p("2. Implemented Class-Balanced Self-Training (CBST), achieving a +4.52% net mIoU gain (+19.31% relative) and boosting rural road recovery by +11.27% without manual rural annotations."))
    story.append(p("3. Validated the methodology on 992 high-resolution validation GeoTIFF rasters, confirming 29.57% calibrated mIoU."))
    story.append(p("4. Built and deployed a live, fully functional cloud GIS platform providing real-time sub-meter hectare quantification."))

    story.append(Paragraph("9.2 Practical Applications for Governance in Mizoram", h2_style))
    story.append(p("• <b>Jhum Shifting Cultivation Monitoring:</b> Quantifies transitions between cleared slopes and active crops, assisting the Department of Agriculture in soil conservation."))
    story.append(p("• <b>Rural Road Infrastructure Planning:</b> Automated mapping of remote cut-slope tracks and landslides across monsoon-affected terrain."))
    story.append(p("• <b>Hydrological Basin Management:</b> Identifies riverbed narrowing and alluvial sediment accumulation across rural drainage channels."))

    story.append(Paragraph("9.3 Future Research Directions", h2_style))
    story.append(p(
        "Future enhancements will focus on integrating multi-temporal Sentinel-2 optical and Sentinel-1 Synthetic Aperture Radar (SAR) time-series to monitor "
        "vegetation regrowth through dense monsoon cloud cover. Additionally, integrating the Segment Anything Model (SAM) with prompt-based fine-tuning represents "
        "a compelling avenue for zero-shot geospatial generalization."
    ))
    story.append(PageBreak())

    # ==========================
    # REFERENCES (IEEE)
    # ==========================
    story.append(Paragraph("REFERENCES", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#1E3A8A"), spaceBefore=2, spaceAfter=10))

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
        story.append(Paragraph(r, ParagraphStyle('RefP', fontName='Times-Roman', fontSize=8, leading=11, spaceAfter=4)))

    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"[SUCCESS] PDF generated successfully: {output_pdf}")
    return output_pdf

if __name__ == "__main__":
    build_pdf()
