from sqlalchemy import BigInteger, Column, DateTime, String, Text
from sqlalchemy.dialects.mysql import JSON

from db_model.base import Base


class DwdPatent(Base):
    __tablename__ = "dwd_patent"

    patent_id = Column(String(64), primary_key=True, comment="专利记录唯一标识")
    publication_number = Column(String(64), nullable=False, comment="专利公布号")
    application_kind = Column(String(2), comment="专利申请类型代码")
    country_code = Column(String(2), comment="国家、地区或组织代码")
    country = Column(String(20), comment="专利所属或发布的国家名称")
    publication_reference = Column(JSON, comment="发布文献种类代码、发布日期、年份和年月")
    application_reference = Column(JSON, comment="申请号、受理局代码、申请日期、年份和年月")
    pct_or_regional_filing_data = Column(JSON, comment="PCT 申请号和申请日期")
    pct_or_regional_publishing_data = Column(JSON, comment="PCT 公布号和公布日期")
    priority_filings = Column(JSON, comment="优先权信息对象数组")
    applicants = Column(JSON, comment="原始申请人对象数组")
    assignees = Column(JSON, comment="当前申请人或专利权人对象数组")
    inventors = Column(JSON, comment="发明人对象数组")
    first_applicant_name = Column(String(255), comment="第一原始申请人")
    first_current_assignee_name = Column(String(255), comment="第一当前申请人或专利权人")
    first_inventor_name = Column(String(255), comment="第一发明人")
    classification_ipcr = Column(JSON, comment="IPCR/IPC 主分类号和附加分类号")
    classification_cpc = Column(JSON, comment="CPC 主分类号和附加分类号")
    keywords = Column(Text, comment="描述专利主题内容的关键词")
    claims_localized = Column(Text, comment="专利权利要求书的文本内容")
    description_localized = Column(Text, comment="专利说明书的正文内容")
    figures = Column(Text, comment="专利附图或图示相关信息")
    language = Column(String(16), comment="专利原始文本使用的语言")
    granted_number = Column(String(64), comment="专利授权编号")
    spif_application_number = Column(String(64), comment="SPIF 标准申请号")
    spif_publication_number = Column(String(64), comment="SPIF 标准公布号")
    prior_art_year = Column(String(4), comment="相关现有技术对应的年份")
    prior_art_date = Column(String(10), comment="相关现有技术对应的日期")
    relevants = Column(Text, comment="相关专利信息")
    db_source = Column(String(64), nullable=False, comment="数据来源贴源库")
    create_time = Column(DateTime, nullable=False, comment="记录创建时间")
    update_time = Column(DateTime, nullable=False, comment="记录最近更新时间")
    citation_nums = Column(BigInteger, comment="引用专利数量")
    patent_citations = Column(JSON, comment="引用专利对象数组")
    cited_by_nums = Column(BigInteger, comment="被引专利数量")
    cited_by = Column(JSON, comment="被引专利对象数组")
    non_patent_citations_nums = Column(BigInteger, comment="非专利文献引用数量")
    non_patent_citations = Column(JSON, comment="非专利文献引用对象数组")
    dates_of_public_availability = Column(JSON, comment="授权日期、年份和年月")
    status = Column(String(10), comment="专利当前法律状态")
    anticipated_expiration = Column(String(10), comment="预计到期日")
    expiration_year = Column(String(10), comment="预计或实际到期年份")
    family_citations = Column(Text, comment="家族内引用信息")
    cited_by_family = Column(Text, comment="家族内被引用信息")
    other_versions = Column(Text, comment="其他公开、公告或授权版本")
    worldwides = Column(Text, comment="全球同族专利信息")
    simple_family = Column(JSON, comment="简单同族成员文献号")


class DwdPatentTitle(Base):
    __tablename__ = "dwd_patent_title"

    patent_id = Column(String(64), primary_key=True, comment="关联专利唯一标识")
    title_localized = Column(JSON, comment="原文标题和英文标题")
    db_source = Column(String(64), nullable=False, comment="数据来源贴源库")
    create_time = Column(DateTime, nullable=False, comment="记录创建时间")
    update_time = Column(DateTime, nullable=False, comment="记录最近更新时间")


class DwdPatentAbstract(Base):
    __tablename__ = "dwd_patent_abstract"

    patent_id = Column(String(64), primary_key=True, comment="关联专利唯一标识")
    abstract_localized = Column(JSON, comment="原文摘要和英文摘要")
    db_source = Column(String(64), nullable=False, comment="数据来源贴源库")
    create_time = Column(DateTime, nullable=False, comment="记录创建时间")
    update_time = Column(DateTime, nullable=False, comment="记录最近更新时间")


class DwdPatentLegal(Base):
    __tablename__ = "dwd_patent_legal"

    patent_id = Column(String(64), primary_key=True, comment="关联专利唯一标识")
    legal_events = Column(Text, comment="专利生命周期中的法律状态变更事件")
    prs_data = Column("patent_legal/prs_data", JSON, comment="PRS 事件日期、代码和法律状态分类说明")
    db_source = Column(String(64), nullable=False, comment="数据来源贴源库")
    create_time = Column(DateTime, nullable=False, comment="记录创建时间")
    update_time = Column(DateTime, nullable=False, comment="记录最近更新时间")


class DwdPatentFamily(Base):
    __tablename__ = "dwd_patent_family"

    patent_id = Column(String(64), primary_key=True, comment="关联专利唯一标识")
    simple_family = Column(JSON, comment="专利家族 ID、成员国家代码和文献种类代码")
    db_source = Column(String(64), nullable=False, comment="数据来源贴源库")
    create_time = Column(DateTime, nullable=False, comment="记录创建时间")
    update_time = Column(DateTime, nullable=False, comment="记录最近更新时间")
