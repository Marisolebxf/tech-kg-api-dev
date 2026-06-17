from sqlalchemy import BigInteger, Column, Date, DateTime, Numeric, String, Text

from db_model.base import Base


class DwdIndustryChainInfo(Base):
    __tablename__ = "dwd_industry_chain_info"

    chain_code = Column(String(255), primary_key=True, comment="产业链唯一id")
    chain_name = Column(String(255), nullable=False, comment="产业链名称")
    node_id = Column(String(255), primary_key=True, comment="产业链节点唯一id")
    node_name = Column(String(255), nullable=False, comment="节点名称")
    node_type = Column(BigInteger, nullable=False, comment="1-大类节点 2-业务节点 3-展示节点")
    level = Column(BigInteger, nullable=False, comment="节点所处层级")
    node_seq = Column(BigInteger, comment="同一父级节点下的子节点排序参考值")
    parent_id = Column(String(255), comment="父级节点id")
    parent_name = Column(Text, comment="父级节点名称")
    node_imp_level = Column(BigInteger, comment="节点重要性，1最高5最低")
    downstream_link_code = Column(String(255), comment="下游关联节点id")
    node_stage = Column(BigInteger, comment="1-上游 2-中游 3-下游")
    node_path = Column(Text, comment="节点路径")
    data_source = Column(String(255), nullable=False, comment="数据来源")
    created_time = Column(DateTime, nullable=False, comment="创建时间")
    updated_time = Column(DateTime, nullable=False, comment="更新时间")


class DwdOrgIndustryChainDtl(Base):
    __tablename__ = "dwd_org_industry_chain_dtl"

    chain_code = Column(String(255), primary_key=True, comment="产业链唯一id")
    chain_name = Column(String(255), nullable=False, comment="产业链名称")
    node_id = Column(String(255), primary_key=True, comment="产业链节点唯一id")
    node_name = Column(String(255), nullable=False, comment="节点名称")
    antitypic = Column(String(255), primary_key=True, comment="企业身份唯一id")
    credit_code = Column(String(255), comment="统一社会信用代码")
    chain_score = Column(Numeric(20, 2), comment="产业链评分")
    data_source = Column(String(255), nullable=False, comment="数据来源")
    created_time = Column(DateTime, nullable=False, comment="创建时间")
    updated_time = Column(DateTime, nullable=False, comment="更新时间")


class DwdOrgIndustryChainProdDtl(Base):
    __tablename__ = "dwd_org_industry_chain_prod_dtl"

    chain_code = Column(String(255), primary_key=True, comment="产业链唯一id")
    chain_name = Column(String(255), nullable=False, comment="产业链名称")
    antitypic = Column(String(255), primary_key=True, comment="企业身份唯一id")
    company_name = Column(String(500), comment="企业名称")
    credit_code = Column(String(255), comment="统一社会信用代码")
    tech_product = Column(String(255), primary_key=True, comment="主营产品名称")
    tech_product_seq = Column(BigInteger, comment="主营产品排序")
    data_source = Column(String(255), nullable=False, comment="数据来源")
    created_time = Column(DateTime, nullable=False, comment="创建时间")
    updated_time = Column(DateTime, nullable=False, comment="更新时间")


class DwdIndustryChainNewsInfo(Base):
    __tablename__ = "dwd_industry_chain_news_info"

    chain_code = Column(String(255), primary_key=True, comment="产业链唯一id")
    chain_name = Column(String(255), nullable=False, comment="产业链名称")
    news_id = Column(String(255), primary_key=True, comment="资讯唯一id")
    title = Column(String(255), comment="标题")
    relaese_date = Column(Date, comment="发布时间")
    summary = Column(Text, comment="摘要")
    source = Column(String(255), comment="来源")
    data_source = Column(String(255), nullable=False, comment="数据来源")
    created_time = Column(DateTime, nullable=False, comment="创建时间")
    updated_time = Column(DateTime, nullable=False, comment="更新时间")
