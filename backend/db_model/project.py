from sqlalchemy import Column, Date, DateTime, Enum, Integer, Numeric, String, Text
from sqlalchemy.dialects.mysql import JSON, LONGTEXT

from db_model.base import Base


class DwdZhProject(Base):
    __tablename__ = "dwd_zh_project"

    id = Column(String(64), primary_key=True, comment="项目记录的唯一主键标识")
    project_number = Column(String(64), comment="项目在管理系统中的编号")
    title = Column(String(512), comment="项目的名称或标题")
    project_source = Column(String(64), comment="项目所属的资助来源或立项来源")
    funded_institution = Column(String(128), comment="获得项目资助的机构名称")
    project_level = Column(
        Enum("国家级", "省级", "市级", "县级", "其他"), comment="项目所属的级别或层次"
    )
    funded_amount = Column(Numeric(18, 2), comment="项目获得的资助经费金额，单位为万元")
    discipline = Column(String(256), comment="项目所属的学科领域")
    discipline_code = Column(String(256), comment="项目所属学科的分类代码")
    fund_category = Column(String(64), comment="项目对应的基金或资助类别")
    funded_province = Column(String(32), comment="项目受资助机构所在的省份")
    participating_institution = Column(JSON, comment="参与项目研究或实施的机构信息")
    approval_year = Column(Integer, comment="项目获批立项的年份")
    approval_time = Column(Date, comment="项目正式获批立项的时间")
    research_period = Column(String(64), comment="项目计划开展研究的时间期限")
    project_host = Column(String(16), comment="项目的主要负责人或主持人")
    participants = Column(JSON, comment="参与项目研究或实施的人员信息")
    keywords = Column(JSON, comment="描述项目研究主题的关键词")
    abstract = Column(LONGTEXT, comment="项目申请书或标书中的摘要内容")
    final_report_abstract = Column(LONGTEXT, comment="项目结题报告中的摘要内容")
    project_page_url = Column(Text, comment="项目详情页面的访问链接")
    updated_time = Column(DateTime, nullable=False, comment="该条数据最近一次更新的时间")


class DwdZhProjectOutput(Base):
    __tablename__ = "dwd_zh_project_output"

    id = Column(String(64), primary_key=True, comment="项目记录的唯一主键标识")
    total_outputs = Column(Integer, comment="项目产生的成果总数量")
    journal_articles_count = Column(Integer, comment="项目产出的期刊论文数量")
    conference_papers_count = Column(Integer, comment="项目产出的会议论文数量")
    degree_papers_count = Column(Integer, comment="项目产出的学位论文数量")
    patents_count = Column(Integer, comment="项目产出的专利数量")
    books_count = Column(Integer, comment="项目产出的图书或专著数量")
    awards_count = Column(Integer, comment="项目获得的奖项数量")
    reports_count = Column(Integer, comment="项目产出的报告数量")
    other_outputs_count = Column(Integer, comment="项目产生的其他成果数量")
    output_journal_articles = Column(JSON, comment="项目产出的期刊文章内容")
    output_patents = Column(JSON, comment="项目产出专利标题")
    output_conference_papers = Column(JSON, comment="项目产出会议论文标题")
    output_degree_papers = Column(JSON, comment="项目产出学位论文标题")
    output_clinical_trials = Column(JSON, comment="项目产出临床试验标题")
    output_books = Column(JSON, comment="项目产出图书专著标题")
    output_awards = Column(JSON, comment="项目产出奖项标题")
    output_reports = Column(JSON, comment="项目产出报告标题")
    output_other = Column(JSON, comment="项目其他产出标题")
    updated_time = Column(DateTime, nullable=False, comment="该条数据最近一次更新的时间")


class DwdEnProject(Base):
    __tablename__ = "dwd_en_project"

    id = Column(String(64), primary_key=True, comment="项目记录的唯一主键标识")
    project_number = Column(String(32), comment="项目在管理系统中的编号")
    title = Column(String(512), comment="项目的名称或标题")
    project_source = Column(String(64), comment="项目所属的资助来源或立项来源")
    funded_institution = Column(String(128), comment="获得项目资助的机构名称")
    project_level = Column(
        Enum("国家级", "州级", "市级", "县级", "其他"), comment="项目所属的级别或层次"
    )
    funded_amount = Column(Numeric(18, 2), comment="项目获得的资助经费金额，单位为美元")
    discipline = Column(String(256), comment="项目所属的学科领域")
    discipline_code = Column(String(256), comment="项目所属学科的分类代码")
    fund_category = Column(String(64), comment="项目对应的基金或资助类别")
    funded_region = Column(String(32), comment="项目受资助机构所在的地区信息")
    participating_institution = Column(JSON, comment="参与项目研究或实施的机构信息")
    approval_year = Column(Integer, comment="项目获批立项的年份")
    approval_time = Column(Date, comment="项目正式获批立项的时间")
    research_period = Column(String(64), comment="项目计划开展研究的时间期限")
    project_host = Column(String(64), comment="项目的主要负责人或主持人")
    participants = Column(JSON, comment="参与项目研究或实施的人员信息")
    keywords = Column(JSON, comment="描述项目研究主题的关键词")
    abstract = Column(LONGTEXT, comment="项目申请书或标书中的摘要内容")
    final_report_abstract = Column(LONGTEXT, comment="项目结题报告中的摘要内容")
    project_page_url = Column(Text, comment="项目详情页面的访问链接")
    updated_time = Column(DateTime, nullable=False, comment="该条数据最近一次更新的时间")


class DwdEnProjectOutput(Base):
    __tablename__ = "dwd_en_project_output"

    id = Column(String(64), primary_key=True, comment="项目记录的唯一主键标识")
    total_outputs = Column(Integer, comment="项目产生的成果总数量")
    journal_articles_count = Column(Integer, comment="项目产出的期刊论文数量")
    conference_papers_count = Column(Integer, comment="项目产出的会议论文数量")
    degree_papers_count = Column(Integer, comment="项目产出的学位论文数量")
    patents_count = Column(Integer, comment="项目产出的专利数量")
    clinical_trials_count = Column(Integer, comment="项目产出的临床试验数量")
    books_count = Column(Integer, comment="项目产出的图书或专著数量")
    awards_count = Column(Integer, comment="项目获得的奖项数量")
    reports_count = Column(Integer, comment="项目产出的报告数量")
    other_outputs_count = Column(Integer, comment="项目产生的其他成果数量")
    output_journal_articles = Column(JSON, comment="项目产出的期刊文章内容")
    output_patents = Column(JSON, comment="项目产出专利标题")
    output_conference_papers = Column(JSON, comment="项目产出会议论文标题")
    output_degree_papers = Column(JSON, comment="项目产出学位论文标题")
    output_clinical_trials = Column(JSON, comment="项目产出临床试验标题")
    output_books = Column(JSON, comment="项目产出图书专著标题")
    output_awards = Column(JSON, comment="项目产出奖项标题")
    output_reports = Column(JSON, comment="项目产出报告标题")
    output_other = Column(JSON, comment="项目其他产出标题")
    updated_time = Column(DateTime, nullable=False, comment="该条数据最近一次更新的时间")
