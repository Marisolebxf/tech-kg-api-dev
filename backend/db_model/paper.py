from sqlalchemy import BigInteger, Column, DateTime, Double, Integer, SmallInteger, String, Text
from sqlalchemy.dialects.mysql import JSON, LONGTEXT, YEAR

from db_model.base import Base


# ==================== 中文论文 ====================


class DwdZhPaper(Base):
    __tablename__ = "dwd_zh_paper"

    paper_id = Column(String(64), primary_key=True, comment="文献记录的唯一主键标识")
    doi = Column(String(512), comment="论文的唯一标识编码")
    name_en = Column(String(1024), comment="文献的英文标题名称")
    name_zh = Column(String(1024), comment="文献的中文标题名称")
    publication_id = Column(BigInteger, nullable=False, comment="关联出版物的id")
    paper_type = Column(String(255), comment="文献所属出版物的章节名称")
    publication_type = Column(String(255), comment="出版物类别")
    publication_name_zh = Column(String(1024), comment="期刊的中文名称")
    issn = Column(String(16), comment="期刊的国际标准连续出版物编号")
    volume = Column(String(128), comment="文献发表所在期刊的卷号")
    issue = Column(String(128), comment="文献发表所在期刊的期号")
    first_page = Column(String(255), comment="论文在期刊中的起始页码")
    last_page = Column(String(255), comment="论文在期刊中的结束页码")
    publication_year = Column(String(255), comment="文献正式发表的日期")
    publication_date = Column(String(255), comment="文献正式发表的日期")
    language = Column(SmallInteger, comment="期刊出版使用的语言类型")
    abstract_available = Column(String(1), comment="摘要是否可用")
    open_access = Column(SmallInteger, comment="标识期刊或论文是否为开放获取")
    source_url = Column(Text, comment="文献数据的原始来源地址")
    data_source = Column(String(255), nullable=False, comment="来源贴源库表名")
    created_time = Column(DateTime, nullable=False, comment="数据在要素库中的创建时间")
    updated_time = Column(DateTime, nullable=False, comment="该条数据最近一次更新的时间")


class DwdZhPaperTitle(Base):
    __tablename__ = "dwd_zh_paper_title"

    logical_id = Column(String(128), primary_key=True, comment="标题信息表逻辑主键")
    paper_id = Column(String(64), nullable=False, comment="文献记录的唯一主键标识")
    title_sequence = Column(Integer, nullable=False, comment="同一文献多个标题的顺序号")
    name_en = Column(String(1024), comment="文献的英文标题名称")
    name_zh = Column(String(1024), comment="文献的中文标题名称")
    language_code = Column(String(12), comment="标题的语言代码")
    language = Column(String(255), comment="标题的语言类型")
    is_original_title = Column(String(1), comment="是否为原始标题")
    data_source = Column(String(255), nullable=False, comment="来源贴源库表名")
    created_time = Column(DateTime, nullable=False, comment="数据在要素库中的创建时间")
    updated_time = Column(DateTime, nullable=False, comment="该条数据最近一次更新的时间")


class DwdZhPaperAbstract(Base):
    __tablename__ = "dwd_zh_paper_abstract"

    logical_id = Column(String(128), primary_key=True, comment="标题信息表逻辑主键")
    paper_id = Column(String(64), nullable=False, comment="文献记录的唯一主键标识")
    abstract_sequence = Column(Integer, nullable=False, comment="同一文献多个摘要的顺序号")
    language = Column(String(255), comment="文献或期刊出版使用的语言类型")
    is_original_abstract = Column(String(1), nullable=False, comment="是否为原始摘要")
    abstract_en = Column(LONGTEXT, comment="文献内容的英文摘要信息")
    abstract_zh = Column(LONGTEXT, comment="文献内容的中文摘要信息")
    data_source = Column(String(255), nullable=False, comment="来源贴源库表名")
    created_time = Column(DateTime, nullable=False, comment="数据在要素库中的创建时间")
    updated_time = Column(DateTime, nullable=False, comment="该条数据最近一次更新的时间")


class DwdZhPaperAuthor(Base):
    __tablename__ = "dwd_zh_paper_author"

    logical_id = Column(String(128), primary_key=True, comment="标题信息表逻辑主键")
    paper_id = Column(String(64), nullable=False, comment="文献记录的唯一主键标识")
    author_sequence = Column(Integer, nullable=False, comment="作者在文献中的顺序")
    author_id = Column(String(32), nullable=False, comment="文献作者的唯一主键 id")
    author_name_en = Column(String(255), nullable=False, comment="文献作者的英文名称")
    author_name_zh = Column(String(255), comment="文献作者中文名")
    author_email = Column(JSON, comment="文献作者email")
    is_corresponding_author = Column(SmallInteger, comment="是否为通讯作者")
    organization_name = Column(Text, comment="作者所属机构或单位的名称")
    author_address = Column(JSON, comment="文献作者地址")
    data_source = Column(String(255), nullable=False, comment="来源贴源库表名")
    created_time = Column(DateTime, nullable=False, comment="数据在要素库中的创建时间")
    updated_time = Column(DateTime, nullable=False, comment="该条数据最近一次更新的时间")


class DwdZhJournal(Base):
    __tablename__ = "dwd_zh_journal"

    logical_id = Column(String(128), primary_key=True, comment="标题信息表逻辑主键")
    paper_id = Column(String(64), nullable=False, comment="文献记录的唯一主键标识")
    journal_id = Column(BigInteger, nullable=False, comment="期刊记录的唯一标识")
    publication_type = Column(String(255), comment="出版物类别")
    country = Column(String(255), comment="期刊所属或出版所在的国家")
    journal_name_zh = Column(String(1024), comment="期刊的中文名称")
    journal_abbreviation = Column(String(255), comment="期刊名称的简称或缩写")
    journal_name_en = Column(String(1024), comment="期刊的英文名称")
    iscn = Column(String(16), comment="期刊的国内统一刊号")
    issn = Column(String(16), comment="期刊的国际标准连续出版物编号")
    eissn = Column(String(16), comment="期刊电子版的国际标准连续出版物编号")
    founding_year = Column(Integer, comment="期刊首次创办或发行的时间")
    official_website = Column(Text, comment="期刊官方网站地址")
    description = Column(Text, comment="期刊的中文简介或说明")
    format = Column(String(255), comment="期刊的版面开本规格")
    postal_code = Column(String(32), comment="期刊邮政发行使用的代号")
    chief_editor = Column(String(128), comment="期刊当前或记录中的主编信息")
    organizer = Column(String(1024), comment="负责主办该期刊的单位名称")
    publication_place = Column(String(64), comment="期刊出版发行的地点")
    awards = Column(Text, comment="期刊获得的奖项或荣誉信息")
    citation_count = Column(Integer, comment="期刊或文献的累计被引用次数")
    annual_publication_count = Column(Integer, comment="期刊每年发表文章的数量")
    is_review_journal = Column(SmallInteger, comment="标识该期刊是否为综述类期刊")
    impact_factor = Column(Double, comment="期刊的影响因子指标")
    quartile = Column(SmallInteger, comment="期刊在相关评价体系中的分区信息")
    classification_code = Column(Text, comment="文献或期刊对应的学科分类编号")
    warning_flag = Column(SmallInteger, comment="标识期刊是否处于预警状态")
    sci_flag = Column(SmallInteger, comment="标识期刊是否被 SCI 收录")
    publication_cycle = Column(String(64), comment="期刊的出版频率或发行周期")
    paper_count = Column(Integer, comment="期刊已发表论文的数量")
    data_source = Column(String(255), nullable=False, comment="来源贴源库表名")
    created_time = Column(DateTime, nullable=False, comment="数据在要素库中的创建时间")
    updated_time = Column(DateTime, nullable=False, comment="该条数据最近一次更新的时间")


class DwdZhPaperReference(Base):
    __tablename__ = "dwd_zh_paper_reference"

    logical_id = Column(String(128), primary_key=True, comment="标题信息表逻辑主键")
    paper_id = Column(String(64), nullable=False, comment="文献记录的唯一主键标识")
    publication_id = Column(BigInteger, nullable=False, comment="关联出版物的id")
    reference_doi = Column(String(512), nullable=False, comment="论文的唯一标识编码")
    reference_name_zh = Column(String(1024), comment="参考文献的中文标题名称")
    reference_publication_name_zh = Column(String(1024), comment="参考文献出版物的中文名称")
    reference_year = Column(YEAR, comment="文献正式发表的年份")
    reference_volume = Column(String(128), comment="参考文献发表所在期刊的卷号")
    reference_issue = Column(String(128), comment="参考文献发表所在期刊的期号")
    reference_first_page = Column(String(255), comment="参考文献在期刊中的起始页码")
    reference_last_page = Column(String(255), comment="参考文献在期刊中的结束页码")
    data_source = Column(String(255), nullable=False, comment="来源贴源库表名")
    created_time = Column(DateTime, nullable=False, comment="数据在要素库中的创建时间")
    updated_time = Column(DateTime, nullable=False, comment="该条数据最近一次更新的时间")


class DwdZhPaperCitation(Base):
    __tablename__ = "dwd_zh_paper_citation"

    logical_id = Column(String(128), primary_key=True, comment="标题信息表逻辑主键")
    paper_id = Column(String(64), nullable=False, comment="文献记录的唯一主键标识")
    publication_id = Column(BigInteger, nullable=False, comment="关联出版物的id")
    citation_doi = Column(String(512), nullable=False, comment="论文的唯一标识编码")
    citation_name_zh = Column(String(1024), comment="引用文献的中文标题名称")
    citation_publication_name_zh = Column(String(1024), comment="参考文献出版物的中文名称")
    data_source = Column(String(255), nullable=False, comment="来源贴源库表名")
    created_time = Column(DateTime, nullable=False, comment="数据在要素库中的创建时间")
    updated_time = Column(DateTime, nullable=False, comment="该条数据最近一次更新的时间")


class DwdZhPaperClassification(Base):
    __tablename__ = "dwd_zh_paper_classification"

    logical_id = Column(String(128), primary_key=True, comment="标题信息表逻辑主键")
    paper_id = Column(String(64), nullable=False, comment="文献记录的唯一主键标识")
    subject_category = Column(String(20), comment="期刊所属的大类学科领域")
    subject_subcategory = Column(String(20), comment="期刊所属的细分学科领域")
    keywords = Column(LONGTEXT, comment="描述论文主题内容的关键词")
    data_source = Column(String(255), nullable=False, comment="来源贴源库表名")
    created_time = Column(DateTime, nullable=False, comment="数据在要素库中的创建时间")
    updated_time = Column(DateTime, nullable=False, comment="该条数据最近一次更新的时间")


class DwdZhPaperRelated(Base):
    __tablename__ = "dwd_zh_paper_related"

    logical_id = Column(String(128), primary_key=True, comment="标题信息表逻辑主键")
    paper_id = Column(String(64), nullable=False, comment="文献记录的唯一主键标识")
    related_papers = Column(JSON, comment="与当前文献内容或主题相关的文献信息")
    related_doi = Column(String(512), nullable=False, comment="论文的唯一标识编码")
    related_name_zh = Column(String(1024), comment="相关文献的中文标题名称")
    data_source = Column(String(255), nullable=False, comment="来源贴源库表名")
    created_time = Column(DateTime, nullable=False, comment="数据在要素库中的创建时间")
    updated_time = Column(DateTime, nullable=False, comment="该条数据最近一次更新的时间")


# ==================== 英文论文 ====================


class DwdEnPaper(Base):
    __tablename__ = "dwd_en_paper"

    paper_id = Column(String(64), primary_key=True, comment="文献记录的唯一主键标识")
    doi = Column(String(512), nullable=False, comment="论文的唯一标识编码")
    name_en = Column(String(1024), comment="文献的英文标题名称")
    name_zh = Column(String(1024), comment="文献的中文标题名称")
    publication_id = Column(BigInteger, nullable=False, comment="关联出版物的id")
    paper_type = Column(String(255), comment="文献所属出版物的章节名称")
    publication_type = Column(String(255), comment="标识出版载体的类型")
    publication_name_en = Column(String(1024), comment="期刊、顶会或预印本平台的英文名称")
    issn = Column(String(16), comment="纸印出版 issn")
    eissn = Column(String(16), comment="在网发行 issn")
    volume = Column(String(128), comment="文献发表所在期刊的卷号")
    issue = Column(String(128), comment="文献发表所在期刊的期号")
    first_page = Column(String(255), comment="论文在期刊中的起始页码")
    last_page = Column(String(255), comment="论文在期刊中的结束页码")
    publication_year = Column(YEAR, comment="文献正式发表的年份")
    publication_date = Column(String(255), comment="文献正式发表的时间")
    language = Column(String(255), comment="文献或期刊出版使用的语言类型")
    abstract_available = Column(String(1), comment="摘要是否可用")
    open_access = Column(SmallInteger, comment="标识期刊或论文是否为开放获取")
    paper_url = Column(Text, comment="文献在官网或来源平台中的访问链接")
    data_source = Column(String(255), nullable=False, comment="来源贴源库表名")
    created_time = Column(DateTime, nullable=False, comment="数据在要素库中的创建时间")
    updated_time = Column(DateTime, nullable=False, comment="该条数据最近一次更新的时间")


class DwdEnPaperTitle(Base):
    __tablename__ = "dwd_en_paper_title"

    logical_id = Column(String(128), primary_key=True, comment="标题信息表逻辑主键")
    paper_id = Column(String(64), nullable=False, comment="文献记录的唯一主键标识")
    title_sequence = Column(Integer, nullable=False, comment="同一文献多个标题的顺序号")
    name_en = Column(String(1024), comment="文献的英文标题名称")
    name_zh = Column(String(1024), comment="文献的中文标题名称")
    language_code = Column(String(12), comment="标题的语言代码")
    language = Column(String(255), comment="标题的语言类型")
    is_original_title = Column(String(1), comment="是否为原始标题")
    data_source = Column(String(255), nullable=False, comment="来源贴源库表名")
    created_time = Column(DateTime, nullable=False, comment="数据在要素库中的创建时间")
    updated_time = Column(DateTime, nullable=False, comment="该条数据最近一次更新的时间")


class DwdEnPaperAbstract(Base):
    __tablename__ = "dwd_en_paper_abstract"

    logical_id = Column(String(128), primary_key=True, comment="标题信息表逻辑主键")
    paper_id = Column(String(64), nullable=False, comment="文献记录的唯一主键标识")
    abstract_sequence = Column(Integer, nullable=False, comment="同一文献多个摘要的顺序号")
    language = Column(String(255), comment="文献或期刊出版使用的语言类型")
    is_original_abstract = Column(String(1), nullable=False, comment="是否为原始摘要")
    abstract_en = Column(LONGTEXT, comment="文献内容的英文摘要信息")
    abstract_zh = Column(LONGTEXT, comment="文献内容的中文摘要信息")
    data_source = Column(String(255), nullable=False, comment="来源贴源库表名")
    created_time = Column(DateTime, nullable=False, comment="数据在要素库中的创建时间")
    updated_time = Column(DateTime, nullable=False, comment="该条数据最近一次更新的时间")


class DwdEnPaperAuthor(Base):
    __tablename__ = "dwd_en_paper_author"

    logical_id = Column(String(128), primary_key=True, comment="标题信息表逻辑主键")
    paper_id = Column(String(64), nullable=False, comment="文献记录的唯一主键标识")
    author_sequence = Column(Integer, nullable=False, comment="作者在文献中的顺序")
    author_id = Column(String(32), nullable=False, comment="文献作者的唯一主键 id")
    author_name_en = Column(String(255), nullable=False, comment="文献作者的英文名称")
    author_name_zh = Column(String(255), comment="文献作者中文名")
    author_email = Column(JSON, comment="文献作者email")
    is_corresponding_author = Column(SmallInteger, comment="是否为通讯作者")
    organization_name = Column(Text, comment="作者所属机构或单位的名称")
    author_address = Column(JSON, comment="文献作者地址")
    data_source = Column(String(255), nullable=False, comment="来源贴源库表名")
    created_time = Column(DateTime, nullable=False, comment="数据在要素库中的创建时间")
    updated_time = Column(DateTime, nullable=False, comment="该条数据最近一次更新的时间")


class DwdEnJournal(Base):
    __tablename__ = "dwd_en_journal"

    logical_id = Column(String(128), primary_key=True, comment="标题信息表逻辑主键")
    paper_id = Column(String(64), nullable=False, comment="文献记录的唯一主键标识")
    journal_id = Column(BigInteger, nullable=False, comment="期刊、会议或预印本记录的唯一标识")
    publication_type = Column(String(255), comment="标识出版载体的类型")
    country = Column(String(255), comment="期刊、会议或出版机构所属的国家或地区")
    journal_name_en = Column(String(1024), comment="期刊、顶会或预印本平台的英文名称")
    journal_abbreviation = Column(String(255), comment="期刊、会议或预印本名称的简称或缩写")
    journal_name_zh = Column(String(1024), comment="期刊、顶会或预印本平台的中文名称")
    issn = Column(String(16), comment="纸印出版 issn")
    eissn = Column(String(16), comment="在网发行 issn")
    official_website = Column(Text, comment="期刊官方网站地址")
    description = Column(Text, comment="期刊、会议或预印本平台的英文简介或说明")
    founding_year = Column(Integer, comment="期刊首次创办或发行的时间")
    annual_publication_count = Column(Integer, comment="期刊或会议每年发表文章的数量")
    is_review_journal = Column(SmallInteger, comment="标识该期刊是否为综述类期刊")
    impact_factor = Column(Double, comment="期刊或会议的影响力评价指标")
    quartile = Column(String(2), comment="期刊在 JCR 等评价体系中的分区信息")
    review_period = Column(String(255), comment="期刊从投稿到审稿完成的平均周期")
    self_citation_rate = Column(Double, comment="期刊文献中自我引用所占的比例")
    top_flag = Column(SmallInteger, comment="标识期刊或会议是否为所在领域的顶级刊物")
    warning_flag = Column(SmallInteger, comment="标识期刊是否处于预警状态")
    sci_flag = Column(SmallInteger, comment="标识期刊是否被 SCI 收录")
    publication_cycle = Column(String(64), comment="期刊的出版频率或发行周期")
    layout_cost = Column(String(15), comment="期刊发表论文所需的版面费用")
    paper_count = Column(Integer, comment="期刊、会议或平台已发表论文的数量")
    data_source = Column(String(255), nullable=False, comment="来源贴源库表名")
    created_time = Column(DateTime, nullable=False, comment="数据在要素库中的创建时间")
    updated_time = Column(DateTime, nullable=False, comment="该条数据最近一次更新的时间")


class DwdEnPaperReference(Base):
    __tablename__ = "dwd_en_paper_reference"

    logical_id = Column(String(128), primary_key=True, comment="标题信息表逻辑主键")
    paper_id = Column(String(64), nullable=False, comment="文献记录的唯一主键标识")
    publication_id = Column(BigInteger, nullable=False, comment="关联出版物的id")
    reference_doi = Column(String(512), nullable=False, comment="论文的唯一标识编码")
    reference_name_en = Column(String(1024), comment="参考文献的英文标题名称")
    reference_publication_name_en = Column(String(1024), comment="参考文献出版物的英文名称")
    publication_year = Column(YEAR, comment="文献正式发表的年份")
    reference_volume = Column(String(128), comment="参考文献发表所在期刊的卷号")
    reference_issue = Column(String(128), comment="参考文献发表所在期刊的期号")
    reference_first_page = Column(String(255), comment="参考文献在期刊中的起始页码")
    reference_last_page = Column(String(255), comment="参考文献在期刊中的结束页码")
    data_source = Column(String(255), nullable=False, comment="来源贴源库表名")
    created_time = Column(DateTime, nullable=False, comment="数据在要素库中的创建时间")
    updated_time = Column(DateTime, nullable=False, comment="该条数据最近一次更新的时间")


class DwdEnPaperCitation(Base):
    __tablename__ = "dwd_en_paper_citation"

    logical_id = Column(String(128), primary_key=True, comment="标题信息表逻辑主键")
    paper_id = Column(String(64), nullable=False, comment="文献记录的唯一主键标识")
    publication_id = Column(BigInteger, nullable=False, comment="关联出版物的id")
    citation_doi = Column(String(512), nullable=False, comment="论文的唯一标识编码")
    citation_name_en = Column(String(1024), comment="引用文献的英文标题名称")
    citation_publication_name_en = Column(String(1024), comment="参考文献出版物的英文名称")
    data_source = Column(String(255), nullable=False, comment="来源贴源库表名")
    created_time = Column(DateTime, nullable=False, comment="数据在要素库中的创建时间")
    updated_time = Column(DateTime, nullable=False, comment="该条数据最近一次更新的时间")


class DwdEnPaperFunding(Base):
    __tablename__ = "dwd_en_paper_funding"

    logical_id = Column(String(128), primary_key=True, comment="标题信息表逻辑主键")
    paper_id = Column(String(64), nullable=False, comment="文献记录的唯一主键标识")
    funding = Column(LONGTEXT, comment="支持该论文研究的基金或资助项目信息")
    data_source = Column(String(255), nullable=False, comment="来源贴源库表名")
    created_time = Column(DateTime, nullable=False, comment="数据在要素库中的创建时间")
    updated_time = Column(DateTime, nullable=False, comment="该条数据最近一次更新的时间")


class DwdEnPaperClassification(Base):
    __tablename__ = "dwd_en_paper_classification"

    logical_id = Column(String(128), primary_key=True, comment="标题信息表逻辑主键")
    paper_id = Column(String(64), nullable=False, comment="文献记录的唯一主键标识")
    subject_category = Column(String(20), comment="期刊或会议所属的大类学科领域")
    subject_subcategory = Column(String(20), comment="期刊或会议所属的细分学科主题")
    keywords = Column(LONGTEXT, comment="描述论文主题内容的关键词")
    data_source = Column(String(255), nullable=False, comment="来源贴源库表名")
    created_time = Column(DateTime, nullable=False, comment="数据在要素库中的创建时间")
    updated_time = Column(DateTime, nullable=False, comment="该条数据最近一次更新的时间")


class DwdEnPaperRelated(Base):
    __tablename__ = "dwd_en_paper_related"

    logical_id = Column(String(128), primary_key=True, comment="标题信息表逻辑主键")
    paper_id = Column(String(64), nullable=False, comment="文献记录的唯一主键标识")
    related_papers = Column(JSON, comment="与当前文献内容或主题相关的文献信息")
    related_doi = Column(String(512), nullable=False, comment="论文的唯一标识编码")
    related_name_en = Column(String(1024), comment="相关文献的英文标题名称")
    data_source = Column(String(255), nullable=False, comment="来源贴源库表名")
    created_time = Column(DateTime, nullable=False, comment="数据在要素库中的创建时间")
    updated_time = Column(DateTime, nullable=False, comment="该条数据最近一次更新的时间")
