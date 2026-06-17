from sqlalchemy import BigInteger, Column, Date, DateTime, Numeric, String, Text

from db_model.base import Base


# ==================== 国内机构 ====================


class DwdOrgRegInfo(Base):
    __tablename__ = "dwd_org_reg_info"

    org_id = Column(String(255), primary_key=True, comment="机构身份唯一id")
    name_cn = Column(String(255), nullable=False, comment="机构名称")
    external_id = Column(String(255), comment="统一社会信用代码")
    province = Column(String(255), comment="所在省份")
    city = Column(String(255), comment="所在城市")
    address = Column(Text, comment="公司地址")
    addr_lng = Column(String(255), comment="地址对应经度")
    addr_lat = Column(String(255), comment="地址对应维度")
    postal_code = Column(String(255), comment="邮政编码")
    phone = Column(String(255), comment="联系电话")
    email = Column(Text, comment="电子邮箱")
    lerep = Column(String(255), comment="法人名字")
    org_type = Column(String(255), comment="机构类型")
    org_size = Column(String(255), comment="企业规模")
    registration_org = Column(String(255), comment="登记机关")
    incorporation_year = Column(BigInteger, comment="成立年份")
    incorporation_date = Column(Date, comment="成立日期")
    start_date = Column(String(255), comment="经营期限自")
    end_date = Column(String(255), comment="经营期限至")
    listing_status = Column(String(255), comment="上市状态")
    listing_date = Column(Date, comment="上市日期")
    registered_capital_value = Column(Numeric(20, 2), comment="注册资本(本币元)")
    capital_currency_code = Column(String(255), comment="资本货币代码")
    data_source = Column(String(255), nullable=False, comment="数据来源")
    created_time = Column(DateTime, nullable=False, comment="创建时间")
    updated_time = Column(DateTime, nullable=False, comment="更新时间")


class DwdOrgShareholderInfo(Base):
    __tablename__ = "dwd_org_shareholder_info"

    org_id = Column(String(255), primary_key=True, comment="机构身份唯一id")
    name_cn = Column(String(255), nullable=False, comment="机构名称")
    external_id = Column(String(255), comment="统一社会信用代码")
    inv_org_id = Column(String(255), comment="投资方机构id")
    owners_name = Column(String(255), primary_key=True, comment="股东名称")
    owners_type = Column(String(255), comment="股东类型")
    ownership_percentage = Column(Numeric(20, 2), comment="所有权占比(%)")
    data_source = Column(String(255), nullable=False, comment="数据来源")
    created_time = Column(DateTime, nullable=False, comment="创建时间")
    updated_time = Column(DateTime, nullable=False, comment="更新时间")


class DwdOrgExecutiveInfo(Base):
    __tablename__ = "dwd_org_executive_info"

    org_id = Column(String(255), primary_key=True, comment="机构身份唯一id")
    name_cn = Column(String(255), nullable=False, comment="机构名称")
    external_id = Column(String(255), comment="统一社会信用代码")
    executives_name = Column(String(255), primary_key=True, comment="高管姓名")
    executives_position = Column(String(255), comment="职位名称")
    data_source = Column(String(255), nullable=False, comment="数据来源")
    created_time = Column(DateTime, nullable=False, comment="创建时间")
    updated_time = Column(DateTime, nullable=False, comment="更新时间")


class DwdOrgOrgProductInfo(Base):
    __tablename__ = "dwd_org_org_product_info"

    org_id = Column(String(255), primary_key=True, comment="机构身份唯一id")
    name_cn = Column(String(255), nullable=False, comment="机构名称")
    external_id = Column(String(255), comment="统一社会信用代码")
    industry_class = Column(String(255), nullable=False, comment="公司行业分类")
    main_activities = Column(Text, comment="公司经营范围")
    description = Column(Text, comment="业务描述")
    main_prod = Column(String(255), comment="主要产品")
    data_source = Column(String(255), nullable=False, comment="数据来源")
    created_time = Column(DateTime, nullable=False, comment="创建时间")
    updated_time = Column(DateTime, nullable=False, comment="更新时间")


class DwdOrgAnnualFinancialInfo(Base):
    __tablename__ = "dwd_org_annual_financial_info"

    org_id = Column(String(255), primary_key=True, comment="机构身份唯一id")
    name_cn = Column(String(255), nullable=False, comment="机构名称")
    external_id = Column(String(255), comment="统一社会信用代码")
    year = Column(BigInteger, primary_key=True, comment="年报年度")
    total_assets = Column(String(255), comment="资产总额")
    total_liabilities = Column(String(255), comment="负债总额")
    operating_revenue = Column(String(255), comment="营业收入")
    main_business_revenue = Column(String(255), comment="主营业务收入")
    total_profit = Column(String(255), comment="利润总额")
    pure_profit = Column(String(255), comment="净利润")
    total_tax_paid = Column(String(255), comment="纳税总额")
    owners_equity = Column(String(255), comment="所有者权益合计")
    employees_number = Column(String(255), comment="从业人数")
    data_source = Column(String(255), nullable=False, comment="数据来源")
    created_time = Column(DateTime, nullable=False, comment="创建时间")
    updated_time = Column(DateTime, nullable=False, comment="更新时间")


class DwdOrgImportantNewsInfo(Base):
    __tablename__ = "dwd_org_important_news_info"

    org_id = Column(String(255), primary_key=True, comment="机构身份唯一id")
    name_cn = Column(String(255), nullable=False, comment="机构名称")
    external_id = Column(String(255), comment="统一社会信用代码")
    news_title = Column(Text, comment="资讯标题")
    news_date = Column(Date, comment="资讯日期")
    news_content = Column(Text, comment="资讯内容")
    original_textlink = Column(Text, comment="咨询原文链接")
    data_source = Column(String(255), nullable=False, comment="数据来源")
    created_time = Column(DateTime, nullable=False, comment="创建时间")
    updated_time = Column(DateTime, nullable=False, comment="更新时间")


class DwdOrgChangerecordInfo(Base):
    __tablename__ = "dwd_org_changerecord_info"

    org_id = Column(String(255), primary_key=True, comment="机构身份唯一id")
    name_cn = Column(String(255), nullable=False, comment="机构名称")
    external_id = Column(String(255), comment="统一社会信用代码")
    update_content = Column(String(255), nullable=False, comment="变更类型")
    current_name = Column(Text, comment="变更前内容")
    update_name = Column(Text, comment="变更后内容")
    update_date = Column(Date, primary_key=True, comment="变更日期")
    data_source = Column(String(255), nullable=False, comment="数据来源")
    created_time = Column(DateTime, nullable=False, comment="创建时间")
    updated_time = Column(DateTime, nullable=False, comment="更新时间")


class DwdOrgMergerAcquisitionInfo(Base):
    __tablename__ = "dwd_org_merger_acquisition_info"

    acquiring_org_id = Column(String(255), primary_key=True, comment="发起收购企业id")
    acquiring_name = Column(String(255), nullable=False, comment="发起收购企业名称")
    acquired_org_id = Column(String(255), primary_key=True, comment="被收购企业id")
    acquired_name = Column(String(255), nullable=False, comment="被收购企业名称")
    ma_amount = Column(Numeric(20, 2), comment="并购金额(元)")
    currency_code = Column(String(255), comment="并购金额币种")


class DwdOrgFinancingInfo(Base):
    __tablename__ = "dwd_org_financing_info"

    org_id = Column(String(255), primary_key=True, comment="机构身份唯一id")
    name_cn = Column(String(255), nullable=False, comment="机构名称")
    external_id = Column(String(255), comment="统一社会信用代码")
    funding_round = Column(String(255), comment="融资轮次")
    funding_amount = Column(Numeric(20, 2), comment="获投金额(元)")
    funding_currency_code = Column(String(255), comment="金额币种")
    post_valuation = Column(Numeric(20, 2), comment="投后估值")
    completion_date = Column(Date, comment="融资完成时间")
    investors_name = Column(Text, nullable=False, comment="投资方列表")
    data_source = Column(String(255), nullable=False, comment="数据来源")
    created_time = Column(DateTime, nullable=False, comment="创建时间")
    updated_time = Column(DateTime, nullable=False, comment="更新时间")


class DwdOrgInvestInfo(Base):
    __tablename__ = "dwd_org_invest_info"

    org_id = Column(String(255), primary_key=True, comment="机构身份唯一id")
    name_cn = Column(String(255), nullable=False, comment="机构名称")
    external_id = Column(String(255), comment="统一社会信用代码")
    inv_org_id = Column(String(255), primary_key=True, comment="被投资企业id")
    inv_name = Column(String(255), nullable=False, comment="被投资企业名称")
    inv_external_id = Column(String(255), comment="被投资企业统一社会信用代码")
    investment_amount = Column(Numeric(20, 2), comment="投资金额(元)")
    investment_ratio = Column(Numeric(20, 2), comment="股权占比(%)")
    data_source = Column(String(255), nullable=False, comment="数据来源")
    created_time = Column(DateTime, nullable=False, comment="创建时间")
    updated_time = Column(DateTime, nullable=False, comment="更新时间")


class DwdOrgBidInfo(Base):
    __tablename__ = "dwd_org_bid_info"

    tender_org_id = Column(String(255), primary_key=True, comment="采购单位id")
    tender_name_cn = Column(String(255), nullable=False, comment="采购单位名称")
    tender_external_id = Column(String(255), comment="采购单位统一社会信用代码")
    winner_org_id = Column(String(255), primary_key=True, comment="中标单位id")
    winner_name_cn = Column(String(255), nullable=False, comment="中标单位名称")
    winner_external_id = Column(String(255), comment="中标单位统一社会信用代码")
    announcement_title = Column(Text, comment="公告标题")
    announcement_content = Column(Text, comment="中标成交信息")
    data_source = Column(String(255), nullable=False, comment="数据来源")
    created_time = Column(DateTime, nullable=False, comment="创建时间")
    updated_time = Column(DateTime, nullable=False, comment="更新时间")


class DwdOrgRecruitInfo(Base):
    __tablename__ = "dwd_org_recruit_info"

    org_id = Column(String(255), primary_key=True, comment="机构身份唯一id")
    name_cn = Column(String(255), nullable=False, comment="机构名称")
    external_id = Column(String(255), comment="统一社会信用代码")
    job_title = Column(String(255), comment="岗位")
    job_description = Column(Text, comment="工作描述")
    work_place = Column(Text, comment="工作地点")
    release_date = Column(Date, comment="发布日期")
    hiring_number = Column(BigInteger, comment="招聘人数")
    data_source = Column(String(255), nullable=False, comment="数据来源")
    created_time = Column(DateTime, nullable=False, comment="创建时间")
    updated_time = Column(DateTime, nullable=False, comment="更新时间")


class DwdOrgHelsInfo(Base):
    __tablename__ = "dwd_org_hels_info"

    org_id = Column(String(255), primary_key=True, comment="机构身份唯一id")
    name_cn = Column(String(255), nullable=False, comment="机构名称")
    external_id = Column(String(255), comment="统一社会信用代码")
    org_name = Column(String(255), nullable=False, comment="高校/科研机构名称(中文)")
    org_name_en = Column(String(255), comment="高校/科研机构名称(英文)")
    org_desc = Column(Text, comment="高校/科研机构描述")
    est_year = Column(Date, comment="建立时间")
    address = Column(Text, comment="地址")
    addr_lng = Column(String(255), comment="地址对应经度")
    addr_lat = Column(String(255), comment="地址对应维度")
    province = Column(String(255), comment="地址所在省")
    city = Column(String(255), comment="地址所在市")
    univ_type = Column(String(255), comment="高校类型")
    web_link = Column(Text, comment="官方网址")
    postal_code = Column(String(255), comment="邮政编码")
    email = Column(Text, comment="电子邮箱")
    contact_number = Column(String(255), comment="联系电话")
    fax_number = Column(String(255), comment="传真号码")
    data_source = Column(String(255), nullable=False, comment="数据来源")
    created_time = Column(DateTime, nullable=False, comment="创建时间")
    updated_time = Column(DateTime, nullable=False, comment="更新时间")


class DwdOrgTagInfo(Base):
    __tablename__ = "dwd_org_tag_info"

    org_id = Column(String(255), primary_key=True, comment="机构身份唯一id")
    name_cn = Column(String(255), nullable=False, comment="机构名称")
    external_id = Column(String(255), comment="统一社会信用代码")
    org_tag = Column(String(255), primary_key=True, comment="企业标签")
    tag_level = Column(String(255), nullable=False, comment="级别")
    data_source = Column(String(255), nullable=False, comment="数据来源")
    created_time = Column(DateTime, nullable=False, comment="创建时间")
    updated_time = Column(DateTime, nullable=False, comment="更新时间")


class DwdOrgStockBase(Base):
    __tablename__ = "dwd_org_stock_base"

    stock_code = Column(String(255), primary_key=True, comment="股票代码")
    stock_noun = Column(String(255), comment="股票简称")
    stock_type = Column(String(255), comment="上市板块")
    org_id = Column(String(255), nullable=False, comment="机构身份唯一id")
    name_cn = Column(String(255), nullable=False, comment="机构名称")
    external_id = Column(String(255), comment="统一社会信用代码")
    listed_date = Column(Date, comment="上市日期")
    listed_status = Column(String(255), comment="上市状态")
    data_source = Column(String(255), nullable=False, comment="数据来源")
    created_time = Column(DateTime, nullable=False, comment="创建时间")
    updated_time = Column(DateTime, nullable=False, comment="更新时间")


class DwdOrgStockFinanceInfo(Base):
    __tablename__ = "dwd_org_stock_finance_info"

    org_id = Column(String(255), primary_key=True, comment="机构身份唯一id")
    name_cn = Column(String(255), nullable=False, comment="机构名称")
    stock_code = Column(String(255), nullable=False, comment="股票代码")
    external_id = Column(String(255), comment="统一社会信用代码")
    occur_period = Column(String(255), primary_key=True, comment="数据期")
    total_assets = Column(Numeric(20, 2), comment="资产总额(元)")
    fixed_assets = Column(Numeric(20, 2), comment="固定资产总额(元)")
    total_liabilities = Column(Numeric(20, 2), comment="负债总额(元)")
    operating_revenue = Column(Numeric(20, 2), comment="营业收入(元)")
    main_business_revenue = Column(Numeric(20, 2), comment="主营业务收入(元)")
    total_profit = Column(Numeric(20, 2), comment="利润总额(元)")
    pure_profit = Column(Numeric(20, 2), comment="净利润(元)")
    total_tax_paid = Column(Numeric(20, 2), comment="纳税总额(元)")
    oper_cash_flow = Column(Numeric(20, 2), comment="经营活动现金流(元)")
    owners_equity = Column(Numeric(20, 2), comment="所有者权益合计(元)")
    employees_number = Column(BigInteger, comment="从业人数")
    research_development_amount = Column(Numeric(20, 2), comment="研发投入金额(元)")
    data_source = Column(String(255), nullable=False, comment="数据来源")
    created_time = Column(DateTime, nullable=False, comment="创建时间")
    updated_time = Column(DateTime, nullable=False, comment="更新时间")


# ==================== 海外机构 ====================


class DwdForgBaseInfo(Base):
    __tablename__ = "dwd_forg_base_info"

    org_id = Column(String(255), primary_key=True, comment="机构id")
    name_en = Column(String(255), nullable=False, comment="机构名称")
    name_alias = Column(String(255), comment="机构本地名称")
    country_code = Column(String(255), comment="国家代码")
    country = Column(String(255), comment="国家")
    external_id = Column(Text, comment="当地官方唯一注册码")
    city = Column(String(255), comment="所在城市")
    address = Column(Text, comment="公司地址")
    postal_code = Column(Text, comment="邮政编码")
    phone = Column(String(255), comment="联系电话")
    email = Column(String(255), comment="电子邮箱")
    company_type = Column(Text, comment="企业类型")
    registration_org = Column(Text, comment="注册机构")
    incorporation_year = Column(BigInteger, comment="成立年份")
    incorporation_date = Column(Date, comment="成立日期")
    listing_status = Column(String(255), comment="上市状态")
    registered_capital_value = Column(BigInteger, comment="注册资本")
    registered_capital_currency_code = Column(String(255), comment="注册资本货币代码")
    industry_class = Column(String(255), comment="公司行业分类")
    industry_type = Column(String(255), comment="行业分类标准")


class DwdForgShareholderInfo(Base):
    __tablename__ = "dwd_forg_shareholder_info"

    org_id = Column(String(255), primary_key=True, comment="机构id")
    owners_name = Column(String(255), primary_key=True, comment="股东名称")
    ownership_percentage = Column(Numeric(20, 2), comment="股权占比(%)")
    owners_country_code = Column(String(255), comment="股东所在国家代码")
    owners_country = Column(String(255), comment="股东所在国家")


class DwdForgSubsidiaryInfo(Base):
    __tablename__ = "dwd_forg_subsidiary_info"

    org_id = Column(String(255), primary_key=True, comment="机构id")
    affiliate = Column(String(255), primary_key=True, comment="子公司id")
    affiliates_name = Column(String(255), comment="子公司名称")
    affiliates_country_code = Column(String(255), comment="子公司国家代码")
    affiliates_country = Column(String(255), comment="子公司国家")
    affiliates_company_id = Column(String(255), comment="子公司唯一注册码")


class DwdForgExecutiveInfo(Base):
    __tablename__ = "dwd_forg_executive_info"

    org_id = Column(String(255), primary_key=True, comment="机构id")
    executives_name = Column(String(255), primary_key=True, comment="高管姓名")
    executives_position = Column(String(255), comment="职位名称")
    dm_birthdate = Column(Date, comment="高管出生日期")
    dm_nationalities = Column(String(255), comment="高管国籍")
    dm_biography = Column(String(255), comment="高管履历")


class DwdForgProductInfo(Base):
    __tablename__ = "dwd_forg_product_info"

    org_id = Column(String(255), primary_key=True, comment="机构id")
    description = Column(String(255), comment="业务描述")
    main_products = Column(String(255), comment="主要产品")


class DwdForgBeneficiaryInfo(Base):
    __tablename__ = "dwd_forg_beneficiary_info"

    org_id = Column(String(255), primary_key=True, comment="机构id")
    bo_name = Column(String(255), primary_key=True, comment="受益人名称")
    bo_gender = Column(String(255), comment="受益人性别")
    bo_birthdate = Column(Date, comment="受益人出生日期")
    bo_country_code = Column(String(255), comment="受益人所在国家代码")
    path = Column(String(255), comment="受益人关系路径")
    bo_manager = Column(String(255), comment="受益人是否同时是管理层")
    total_percent = Column(Numeric(20, 2), comment="总持股比例")
    direct_percent = Column(Numeric(20, 2), comment="直接持股比例")
    indirect_percent = Column(Numeric(20, 2), comment="间接持股比例")


class DwdForgActControInfo(Base):
    __tablename__ = "dwd_forg_act_contro_info"

    org_id = Column(String(255), primary_key=True, comment="机构id")
    country_code = Column(String(255), comment="企业国家代码")
    entity_eid = Column(String(255), primary_key=True, comment="实控人ID")
    entity_name = Column(String(255), comment="实控人名称")
    entity_type = Column(String(255), comment="实控人类型")
    entity_country_code = Column(String(255), comment="实控人国家代码")
    direct_pct = Column(String(255), comment="直接持股比例")
    total_pct = Column(String(255), comment="总持股比例")
    direct_pct_num = Column(Numeric(20, 2), comment="直接持股比例数值")
    total_pct_num = Column(Numeric(20, 2), comment="总持股比例数值")
    path = Column(Text, comment="路径")


class DwdForgStockFinInfo(Base):
    __tablename__ = "dwd_forg_stock_fin_info"

    org_id = Column(String(255), primary_key=True, comment="机构id")
    occur_period = Column(Date, primary_key=True, comment="报告期")
    total_assets = Column(Numeric(20, 2), comment="资产总额")
    fixed_assets = Column(Numeric(20, 2), comment="固定资产总额")
    total_liabilities = Column(Numeric(20, 2), comment="负债总额")
    operating_revenue = Column(Numeric(20, 2), comment="营业收入")
    main_business_revenue = Column(Numeric(20, 2), comment="主营业务收入")
    total_profit = Column(Numeric(20, 2), comment="利润总额")
    pure_profit = Column(Numeric(20, 2), comment="净利润")
    total_tax_paid = Column(Numeric(20, 2), comment="企业所得税")
    oper_cash_flow = Column(Numeric(20, 2), comment="经营活动现金流")
    owners_equity = Column(Numeric(20, 2), comment="所有者权益合计")
    employees_number = Column(Numeric(20, 2), comment="从业人数")
    research_development_amount = Column(Numeric(20, 2), comment="研发投入金额")
    research_development_employees_number = Column(Numeric(20, 2), comment="研发人员数")
