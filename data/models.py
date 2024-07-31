# # coding: utf-8
# from sqlalchemy import Column, ForeignKey, Integer, Numeric, String, Table, Text
# from sqlalchemy.orm import relationship
# from sqlalchemy.ext.declarative import declarative_base

# Base = declarative_base()
# metadata = Base.metadata


# t_alltests_test_formats_specimen_types = Table(
#     'alltests_test_formats_specimen_types', metadata,
#     Column('test_name', String(100)),
#     Column('test_format', String(100)),
#     Column('specimen_type', String(50))
# )


# t_category_medicine = Table(
#     'category_medicine', metadata,
#     Column('medcat', Text),
#     Column('category', Text),
#     Column('medicine_name', String(100))
# )


# class ClinicalService(Base):
#     __tablename__ = 'clinical_services'

#     clinical_service = Column(String(50), primary_key=True)

#     conditions = relationship('Condition', secondary='condition_services')


# class ConditionLevel(Base):
#     __tablename__ = 'condition_levels'

#     condition_level = Column(String(25), primary_key=True)


# t_condition_tiers_summary = Table(
#     'condition_tiers_summary', metadata,
#     Column('condition_name', String(100)),
#     Column('lancet_condition_tier', String(45)),
#     Column('condition_level', String(25)),
#     Column('condition_name_lancet', String(100))
# )


# class Dbuser(Base):
#     __tablename__ = 'dbusers'

#     username = Column(String(20), nullable=False)
#     usertype = Column(String(20), nullable=False)
#     description = Column(String, nullable=False)
#     uid = Column(Integer, primary_key=True)


# class EmlCategory1(Base):
#     __tablename__ = 'eml_category_1'

#     eml_category1_name = Column(String(100), primary_key=True)


# class EmlCategory2(Base):
#     __tablename__ = 'eml_category_2'

#     eml_category_2_name = Column(String(100), primary_key=True)


# class EmlCategory3(Base):
#     __tablename__ = 'eml_category_3'

#     eml_category_3_name = Column(String(100), primary_key=True)


# class EmlCategory4(Base):
#     __tablename__ = 'eml_category_4'

#     eml_category_4_name = Column(String(100), primary_key=True)


# class EmlCategory5(Base):
#     __tablename__ = 'eml_category_5'

#     eml_category_5_name = Column(String(100), primary_key=True)


# class EmlCategory6(Base):
#     __tablename__ = 'eml_category_6'

#     eml_category_6_name = Column(String(100), primary_key=True)


# t_emls_combined = Table(
#     'emls_combined', metadata,
#     Column('who_eml_v19', String(3)),
#     Column('who_eml_v20', String(3)),
#     Column('who_eml_v20_core', String(3)),
#     Column('who_eml_v20_complementary', String(3)),
#     Column('india_eml_2015_core', String(3)),
#     Column('ghana_nhis_2018', String(3)),
#     Column('ghana_eml_2010', String(3)),
#     Column('ghana_eml_2017', String(3)),
#     Column('ghana_eml_2017_level', String(5)),
#     Column('ghana_eml_2017_reimbursed', String(3)),
#     Column('notes', String(1000)),
#     Column('medicine_name', String(100)),
#     Column('representative', String(1)),
#     Column('preferred', String(1)),
#     Column('view_order', Integer),
#     Column('ghana_eml_2017_todo', String(4)),
#     Column('uid', Integer),
#     Column('enteredby', String(20)),
#     Column('ghana_nhis_2018_level', String(5)),
#     Column('kenya_eml_2016', String(3)),
#     Column('kenya_eml_2016_level', String(3)),
#     Column('kenya_eml_2016_todo', String(12)),
#     Column('categories_combined', Text),
#     Column('nigeria_eml_2016', String(3)),
#     Column('nigeria_eml_2016_level', String(25)),
#     Column('nigeria_eml_2016_todo', String(12)),
#     Column('nigeria_eml_2016_enteredby', String(20))
# )


# t_emls_combined_edl_dashadmin = Table(
#     'emls_combined_edl_dashadmin', metadata,
#     Column('who_eml_v19', String(3)),
#     Column('who_eml_v20', String(3)),
#     Column('who_eml_v20_core', String(3)),
#     Column('who_eml_v20_complementary', String(3)),
#     Column('india_eml_2015_core', String(3)),
#     Column('ghana_nhis_2018', String(3)),
#     Column('ghana_eml_2010', String(3)),
#     Column('ghana_eml_2017', String(3)),
#     Column('ghana_eml_2017_level', String(5)),
#     Column('ghana_eml_2017_reimbursed', String(3)),
#     Column('notes', String(1000)),
#     Column('medicine_name', String(100)),
#     Column('representative', String(1)),
#     Column('preferred', String(1)),
#     Column('view_order', Integer),
#     Column('ghana_eml_2017_todo', String(4)),
#     Column('uid', Integer),
#     Column('enteredby', String(20)),
#     Column('ghana_nhis_2018_level', String(5)),
#     Column('kenya_eml_2016', String(3)),
#     Column('kenya_eml_2016_level', String(3)),
#     Column('kenya_eml_2016_todo', String(12)),
#     Column('categories_combined', Text),
#     Column('nigeria_eml_2016', String(3)),
#     Column('nigeria_eml_2016_level', String(25)),
#     Column('nigeria_eml_2016_todo', String(12)),
#     Column('nigeria_eml_2016_enteredby', String(20)),
#     Column('indonesia_eml_phc', String)
# )


# t_ethiopia_chai_tiers_with_values = Table(
#     'ethiopia_chai_tiers_with_values', metadata,
#     Column('tier', String(25)),
#     Column('tier_model', String(45)),
#     Column('tier_value', Numeric(10, 0))
# )


# t_ethiopia_standards_tiers_with_values = Table(
#     'ethiopia_standards_tiers_with_values', metadata,
#     Column('tier', String(45)),
#     Column('tier_model', String(45)),
#     Column('tier_value', Numeric(10, 0))
# )


# class GhanaEmlTier(Base):
#     __tablename__ = 'ghana_eml_tiers'

#     ghana_eml_tier = Column(String(10), primary_key=True)


# t_ghana_moh_tiers_with_values = Table(
#     'ghana_moh_tiers_with_values', metadata,
#     Column('tier', String(25)),
#     Column('tier_model', String(45)),
#     Column('tier_value', Numeric(10, 0))
# )


# t_india_edl_tiers_with_values = Table(
#     'india_edl_tiers_with_values', metadata,
#     Column('tier', String(45)),
#     Column('tier_model', String(45)),
#     Column('tier_value', Numeric(10, 0))
# )


# class IndiaEmlTier(Base):
#     __tablename__ = 'india_eml_tiers'

#     india_eml_tier = Column(String(5), primary_key=True)


# t_junk = Table(
#     'junk', metadata,
#     Column('test_name', String(100)),
#     Column('test_name_pretty', String(200)),
#     Column('test_name_short', String(50)),
#     Column('laboratory', String(100)),
#     Column('clinical_chemistry', Integer),
#     Column('us_lab_upper_peninsula1', Integer),
#     Column('us_lab_upper_peninsula2', Integer),
#     Column('india_free_diagnostics', Integer),
#     Column('who_edl_v1', String(3)),
#     Column('india_edl_v1_draft', String(3)),
#     Column('india_edl_v1_sup_draft', String(3)),
#     Column('who_edl_v2', String(3))
# )


# t_kenya_eml_tiers = Table(
#     'kenya_eml_tiers', metadata,
#     Column('kenya_eml_tier', String(5), nullable=False)
# )


# class LaboratorySection(Base):
#     __tablename__ = 'laboratory_sections'

#     lab_section = Column(String(50), primary_key=True)


# t_lad_test = Table(
#     'lad_test', metadata,
#     Column('row.names', Text),
#     Column('whoedlv2', Text),
#     Column('whoedlv2test', Text),
#     Column('eml', Text),
#     Column('ieml', Text),
#     Column('emlghana', Text),
#     Column('emlghananhis', Text),
#     Column('sublist', Text),
#     Column('condition', Text),
#     Column('clinicalservice', Text),
#     Column('medicine', Text),
#     Column('categories', Text),
#     Column('ghanatier', Text),
#     Column('kenyatier', Text),
#     Column('indiatier', Text),
#     Column('nigeriatier', Text),
#     Column('testreason', Text),
#     Column('laboratory', Text),
#     Column('testformat', Text),
#     Column('specimentype', Text),
#     Column('testname', Text),
#     Column('useredl', Text)
# )


# class LancetConditionTier(Base):
#     __tablename__ = 'lancet_condition_tiers'

#     tier = Column(String(45), primary_key=True)


# t_lancet_package_tiers_with_values = Table(
#     'lancet_package_tiers_with_values', metadata,
#     Column('tier', String(25)),
#     Column('tier_model', String(45)),
#     Column('tier_value', Numeric(10, 0))
# )


# t_medicine_indications_with_condition_selections = Table(
#     'medicine_indications_with_condition_selections', metadata,
#     Column('medicine_name', String(100)),
#     Column('medicine_note', String(250)),
#     Column('condition_name', String(100)),
#     Column('condition_note', String(250)),
#     Column('condition_number', String(5)),
#     Column('who_eml_indication', String(1)),
#     Column('india_eml_2015_indication', String(1)),
#     Column('india_eml_2015_indication_only', String(1)),
#     Column('ghana_eml_2017_indication', String(3)),
#     Column('uid', Integer),
#     Column('medicine_category', String(200)),
#     Column('condition_level', String(25)),
#     Column('lancet_gbd', String(3))
# )


# t_medicine_indications_with_condition_selections_v1 = Table(
#     'medicine_indications_with_condition_selections_v1', metadata,
#     Column('medicine_name', String(100)),
#     Column('medicine_note', String(250)),
#     Column('condition_name', String(100)),
#     Column('condition_note', String(250)),
#     Column('condition_number', String(5)),
#     Column('who_eml_indication', String(1)),
#     Column('india_eml_2015_indication', String(1)),
#     Column('india_eml_2015_indication_only', String(1)),
#     Column('ghana_eml_2017_indication', String(3)),
#     Column('uid', Integer),
#     Column('medicine_category', String(200)),
#     Column('condition_level', String(25)),
#     Column('lancet_gbd', String(3))
# )


# t_medicine_indications_with_tiers = Table(
#     'medicine_indications_with_tiers', metadata,
#     Column('medicine_name', String(100)),
#     Column('medicine_note', String(250)),
#     Column('condition_name', String(100)),
#     Column('condition_note', String(250)),
#     Column('condition_number', String(5)),
#     Column('who_eml_indication', String(1)),
#     Column('india_eml_2015_indication', String(1)),
#     Column('india_eml_2015_indication_only', String(1)),
#     Column('ghana_eml_2017_indication', String(3)),
#     Column('uid', Integer),
#     Column('medicine_category', String(200)),
#     Column('ghana_condition_tier', String(25)),
#     Column('india_condition_tier', String(25)),
#     Column('nigeria_condition_tier', String(25)),
#     Column('kenya_condition_tier', String(25)),
#     Column('lancet_gbd', String(3)),
#     Column('lancet_condition_tier', String(45)),
#     Column('condition_level', String(25))
# )


# t_medicine_indications_with_tiers_v1 = Table(
#     'medicine_indications_with_tiers_v1', metadata,
#     Column('medicine_name', String(100)),
#     Column('medicine_note', String(250)),
#     Column('condition_name', String(100)),
#     Column('condition_note', String(250)),
#     Column('condition_number', String(5)),
#     Column('who_eml_indication', String(1)),
#     Column('india_eml_2015_indication', String(1)),
#     Column('india_eml_2015_indication_only', String(1)),
#     Column('ghana_eml_2017_indication', String(3)),
#     Column('uid', Integer),
#     Column('medicine_category', String(200)),
#     Column('condition_level', String(25)),
#     Column('ghana_condition_tier', String(25)),
#     Column('india_condition_tier', String(25)),
#     Column('nigeria_condition_tier', String(25)),
#     Column('kenya_condition_tier', String(25)),
#     Column('lancet_condition_tier', String(45)),
#     Column('lancet_gbd', String(3))
# )


# class Medicine(Base):
#     __tablename__ = 'medicines'

#     medicine_name = Column(String(100), primary_key=True)
#     medicine_name_short = Column(String(50), nullable=False)


# class NigeriaEmlTier(Base):
#     __tablename__ = 'nigeria_eml_tiers'

#     nigeria_eml_tier = Column(String(25), primary_key=True)


# class Picklist(Base):
#     __tablename__ = 'picklists'

#     description = Column(String(200), nullable=False)
#     value = Column(String(12), nullable=False)
#     list = Column(String(25), nullable=False)
#     uid = Column(Integer, primary_key=True)


# t_rwanda_ministerial_order_tiers_with_values = Table(
#     'rwanda_ministerial_order_tiers_with_values', metadata,
#     Column('tier', String(45)),
#     Column('tier_model', String(45)),
#     Column('tier_value', Numeric(10, 0))
# )


# class SpecimenType(Base):
#     __tablename__ = 'specimen_types'

#     specimen_type = Column(String(50), primary_key=True)


# class SublistCategoriesConditionRelated(Base):
#     __tablename__ = 'sublist_categories_condition_related'

#     sublist_category = Column(String(40), primary_key=True)


# class SublistCategoriesMedicineRelated(Base):
#     __tablename__ = 'sublist_categories_medicine_related'

#     sublist_categories = Column(String(50), primary_key=True)


# t_tableau2_t1_ec_join = Table(
#     'tableau2_t1_ec_join', metadata,
#     Column('testname', String(100)),
#     Column('category', String(25)),
#     Column('conditionname', String(100)),
#     Column('testreason', String(75)),
#     Column('testnote', String(1000)),
#     Column('medicineorconditionnote', String(1000)),
#     Column('sublist', String(75)),
#     Column('medicine', String(100)),
#     Column('conditionnotefromusestable', String(250)),
#     Column('medicineusesgeneralnote', String(250)),
#     Column('categories', String(200)),
#     Column('ghana_condition_tier', String(25)),
#     Column('india_condition_tier', String(25)),
#     Column('nigeria_condition_tier', String(25)),
#     Column('kenya_condition_tier', String(25)),
#     Column('who_edl_indications', String(3)),
#     Column('test_name_short', String(50)),
#     Column('test_name_pretty', String(200)),
#     Column('clinical_service', String(100)),
#     Column('who_eml_v19', String(3)),
#     Column('who_eml_v20', String(3)),
#     Column('who_eml_v20_core', String(3)),
#     Column('who_eml_v20_complementary', String(3)),
#     Column('india_eml_2015_core', String(3)),
#     Column('ghana_nhis_2018', String(3)),
#     Column('ghana_eml_2010', String(3)),
#     Column('ghana_eml_2017', String(3)),
#     Column('ghana_eml_2017_level', String(5)),
#     Column('ghana_eml_2017_reimbursed', String(3)),
#     Column('notes', String(1000)),
#     Column('medicine_name', String(100)),
#     Column('representative', String(1)),
#     Column('preferred', String(1)),
#     Column('view_order', Integer),
#     Column('ghana_eml_2017_todo', String(4)),
#     Column('uid', Integer),
#     Column('enteredby', String(20)),
#     Column('ghana_nhis_2018_level', String(5)),
#     Column('kenya_eml_2016', String(3)),
#     Column('kenya_eml_2016_level', String(3)),
#     Column('kenya_eml_2016_todo', String(12)),
#     Column('categories_combined', Text),
#     Column('laboratory', String(100)),
#     Column('nigeria_eml_2016', String(3)),
#     Column('nigeria_eml_2016_level', String(25)),
#     Column('nigeria_eml_2016_todo', String(12)),
#     Column('nigeria_eml_2016_enteredby', String(20)),
#     Column('lancet_gbd', String(3)),
#     Column('lancet_condition_tier', String(45))
# )


# t_tableau2_t1_ec_join_v1 = Table(
#     'tableau2_t1_ec_join_v1', metadata,
#     Column('testname', String(100)),
#     Column('category', String(25)),
#     Column('conditionname', String(100)),
#     Column('conditionlevel', String(25)),
#     Column('testreason', String(75)),
#     Column('testnote', String(1000)),
#     Column('medicineorconditionnote', String(1000)),
#     Column('sublist', String(75)),
#     Column('medicine', String(100)),
#     Column('conditionnotefromusestable', String(250)),
#     Column('medicineusesgeneralnote', String(250)),
#     Column('categories', String(200)),
#     Column('lancet_gbd', String(3)),
#     Column('lancet_condition_tier', String(45)),
#     Column('ghana_condition_tier', String(25)),
#     Column('india_condition_tier', String(25)),
#     Column('nigeria_condition_tier', String(25)),
#     Column('kenya_condition_tier', String(25)),
#     Column('who_edl_indications', String(3)),
#     Column('test_name_short', String(50)),
#     Column('test_name_pretty', String(200)),
#     Column('clinical_service', String(100)),
#     Column('laboratory', String(100)),
#     Column('who_eml_v19', String(3)),
#     Column('who_eml_v20', String(3)),
#     Column('who_eml_v20_core', String(3)),
#     Column('who_eml_v20_complementary', String(3)),
#     Column('india_eml_2015_core', String(3)),
#     Column('ghana_nhis_2018', String(3)),
#     Column('ghana_eml_2010', String(3)),
#     Column('ghana_eml_2017', String(3)),
#     Column('ghana_eml_2017_level', String(5)),
#     Column('ghana_eml_2017_reimbursed', String(3)),
#     Column('notes', String(1000)),
#     Column('medicine_name', String(100)),
#     Column('representative', String(1)),
#     Column('preferred', String(1)),
#     Column('view_order', Integer),
#     Column('ghana_eml_2017_todo', String(4)),
#     Column('uid', Integer),
#     Column('enteredby', String(20)),
#     Column('ghana_nhis_2018_level', String(5)),
#     Column('kenya_eml_2016', String(3)),
#     Column('kenya_eml_2016_level', String(3)),
#     Column('kenya_eml_2016_todo', String(12)),
#     Column('categories_combined', Text),
#     Column('nigeria_eml_2016', String(3)),
#     Column('nigeria_eml_2016_level', String(25)),
#     Column('nigeria_eml_2016_todo', String(12)),
#     Column('nigeria_eml_2016_enteredby', String(20)),
#     Column('lancet_exclude', String(10))
# )


# t_tableau2_t1_ec_join_v1_edl_dashadmin = Table(
#     'tableau2_t1_ec_join_v1_edl_dashadmin', metadata,
#     Column('testname', String(100)),
#     Column('category', String(25)),
#     Column('conditionname', String(100)),
#     Column('conditionlevel', String(25)),
#     Column('testreason', String(75)),
#     Column('testnote', String(1000)),
#     Column('medicineorconditionnote', String(1000)),
#     Column('sublist', String(75)),
#     Column('medicine', String(100)),
#     Column('conditionnotefromusestable', String(250)),
#     Column('medicineusesgeneralnote', String(250)),
#     Column('categories', String(200)),
#     Column('lancet_gbd', String(3)),
#     Column('lancet_condition_tier', String(45)),
#     Column('ghana_condition_tier', String(25)),
#     Column('india_condition_tier', String(25)),
#     Column('nigeria_condition_tier', String(25)),
#     Column('kenya_condition_tier', String(25)),
#     Column('who_edl_indications', String(3)),
#     Column('test_name_short', String(50)),
#     Column('test_name_pretty', String(200)),
#     Column('clinical_service', String(100)),
#     Column('laboratory', String(100)),
#     Column('who_eml_v19', String(3)),
#     Column('who_eml_v20', String(3)),
#     Column('who_eml_v20_core', String(3)),
#     Column('who_eml_v20_complementary', String(3)),
#     Column('india_eml_2015_core', String(3)),
#     Column('ghana_nhis_2018', String(3)),
#     Column('ghana_eml_2010', String(3)),
#     Column('ghana_eml_2017', String(3)),
#     Column('ghana_eml_2017_level', String(5)),
#     Column('ghana_eml_2017_reimbursed', String(3)),
#     Column('notes', String(1000)),
#     Column('medicine_name', String(100)),
#     Column('representative', String(1)),
#     Column('preferred', String(1)),
#     Column('view_order', Integer),
#     Column('ghana_eml_2017_todo', String(4)),
#     Column('uid', Integer),
#     Column('enteredby', String(20)),
#     Column('ghana_nhis_2018_level', String(5)),
#     Column('kenya_eml_2016', String(3)),
#     Column('kenya_eml_2016_level', String(3)),
#     Column('kenya_eml_2016_todo', String(12)),
#     Column('categories_combined', Text),
#     Column('nigeria_eml_2016', String(3)),
#     Column('nigeria_eml_2016_level', String(25)),
#     Column('nigeria_eml_2016_todo', String(12)),
#     Column('nigeria_eml_2016_enteredby', String(20)),
#     Column('lancet_exclude', String(10)),
#     Column('indonesia_eml_phc', String)
# )


# t_tableau3_t2_tjfs_join = Table(
#     'tableau3_t2_tjfs_join', metadata,
#     Column('testname', String(100)),
#     Column('category', String(25)),
#     Column('conditionname', String(100)),
#     Column('conditionlevel', String(25)),
#     Column('testreason', String(75)),
#     Column('testnote', String(1000)),
#     Column('medicineorconditionnote', String(1000)),
#     Column('sublist', String(75)),
#     Column('medicine', String(100)),
#     Column('conditionnotefromusestable', String(250)),
#     Column('medicineusesgeneralnote', String(250)),
#     Column('categories', String(200)),
#     Column('lancet_gbd', String(3)),
#     Column('lancet_condition_tier', String(45)),
#     Column('ghana_condition_tier', String(25)),
#     Column('india_condition_tier', String(25)),
#     Column('nigeria_condition_tier', String(25)),
#     Column('kenya_condition_tier', String(25)),
#     Column('who_edl_indications', String(3)),
#     Column('test_name_short', String(50)),
#     Column('test_name_pretty', String(200)),
#     Column('clinical_service', String(100)),
#     Column('who_eml_v19', String(3)),
#     Column('who_eml_v20', String(3)),
#     Column('who_eml_v20_core', String(3)),
#     Column('who_eml_v20_complementary', String(3)),
#     Column('india_eml_2015_core', String(3)),
#     Column('ghana_nhis_2018', String(3)),
#     Column('ghana_eml_2010', String(3)),
#     Column('ghana_eml_2017', String(3)),
#     Column('ghana_eml_2017_level', String(5)),
#     Column('ghana_eml_2017_reimbursed', String(3)),
#     Column('notes', String(1000)),
#     Column('medicine_name', String(100)),
#     Column('representative', String(1)),
#     Column('preferred', String(1)),
#     Column('view_order', Integer),
#     Column('ghana_eml_2017_todo', String(4)),
#     Column('uid', Integer),
#     Column('enteredby', String(20)),
#     Column('ghana_nhis_2018_level', String(5)),
#     Column('kenya_eml_2016', String(3)),
#     Column('kenya_eml_2016_level', String(3)),
#     Column('kenya_eml_2016_todo', String(12)),
#     Column('categories_combined', Text),
#     Column('who_edl_v2', String(3)),
#     Column('india_edl_v1_draft', String(3)),
#     Column('test_format', String(100)),
#     Column('specimen_type', String(50)),
#     Column('laboratory', String(100)),
#     Column('nigeria_eml_2016', String(3)),
#     Column('nigeria_eml_2016_level', String(25)),
#     Column('nigeria_eml_2016_todo', String(12)),
#     Column('nigeria_eml_2016_enteredby', String(20)),
#     Column('eml_cat_1', Text),
#     Column('india_edl_v1_sup_draft', String(3)),
#     Column('who_edl_v2_tier', String(45)),
#     Column('india_edl_v1', String(3)),
#     Column('india_edl_v1_tier', String(45)),
#     Column('user_edl', String(3)),
#     Column('nigeria_test_tier_capacity', String(45)),
#     Column('ghana_nhis', String(3)),
#     Column('ghana_nhis_reimbursement_usd', String(10)),
#     Column('lancet_test_tier_capacity', String(25)),
#     Column('who_edl_v2_condition', Text),
#     Column('test_format_lancet_tier', String(25)),
#     Column('test_format_lancet_include', String(3)),
#     Column('lancet_indication_exclude', String(10)),
#     Column('condition_name_lancet', String(100)),
#     Column('clinical_chemistry', Integer),
#     Column('higherpriority', String(3)),
#     Column('who_amr_conditions', String)
# )


# t_tableau3_t2_tjfs_join_archive = Table(
#     'tableau3_t2_tjfs_join_archive', metadata,
#     Column('testname', String(100)),
#     Column('category', String(25)),
#     Column('conditionname', String(100)),
#     Column('testreason', String(75)),
#     Column('testnote', String(1000)),
#     Column('medicineorconditionnote', String(1000)),
#     Column('sublist', String(75)),
#     Column('medicine', String(100)),
#     Column('conditionnotefromusestable', String(250)),
#     Column('medicineusesgeneralnote', String(250)),
#     Column('categories', String(200)),
#     Column('ghana_condition_tier', String(25)),
#     Column('india_condition_tier', String(25)),
#     Column('nigeria_condition_tier', String(25)),
#     Column('kenya_condition_tier', String(25)),
#     Column('who_edl_indications', String(3)),
#     Column('test_name_short', String(50)),
#     Column('test_name_pretty', String(200)),
#     Column('clinical_service', String(100)),
#     Column('who_eml_v19', String(3)),
#     Column('who_eml_v20', String(3)),
#     Column('who_eml_v20_core', String(3)),
#     Column('who_eml_v20_complementary', String(3)),
#     Column('india_eml_2015_core', String(3)),
#     Column('ghana_nhis_2018', String(3)),
#     Column('ghana_eml_2010', String(3)),
#     Column('ghana_eml_2017', String(3)),
#     Column('ghana_eml_2017_level', String(5)),
#     Column('ghana_eml_2017_reimbursed', String(3)),
#     Column('notes', String(1000)),
#     Column('medicine_name', String(100)),
#     Column('representative', String(1)),
#     Column('preferred', String(1)),
#     Column('view_order', Integer),
#     Column('ghana_eml_2017_todo', String(4)),
#     Column('uid', Integer),
#     Column('enteredby', String(20)),
#     Column('ghana_nhis_2018_level', String(5)),
#     Column('kenya_eml_2016', String(3)),
#     Column('kenya_eml_2016_level', String(3)),
#     Column('kenya_eml_2016_todo', String(12)),
#     Column('categories_combined', Text),
#     Column('who_edl_v2', String(3)),
#     Column('india_edl_v1_draft', String(3)),
#     Column('test_format', String(100)),
#     Column('specimen_type', String(50)),
#     Column('laboratory', String(100)),
#     Column('nigeria_eml_2016', String(3)),
#     Column('nigeria_eml_2016_level', String(25)),
#     Column('nigeria_eml_2016_todo', String(12)),
#     Column('nigeria_eml_2016_enteredby', String(20)),
#     Column('eml_cat_1', Text),
#     Column('india_edl_v1_sup_draft', String(3)),
#     Column('who_edl_v2_tier', String(45)),
#     Column('india_edl_v1', String(3)),
#     Column('india_edl_v1_tier', String(45)),
#     Column('user_edl', String(3)),
#     Column('nigeria_test_tier_capacity', String(45)),
#     Column('ghana_nhis', String(3)),
#     Column('ghana_nhis_reimbursement_usd', String(10)),
#     Column('lancet_gbd', String(3)),
#     Column('lancet_condition_tier', String(45))
# )


# t_tableau3_t2_tjfs_join_edl_dashadmin = Table(
#     'tableau3_t2_tjfs_join_edl_dashadmin', metadata,
#     Column('testname', String(100)),
#     Column('category', String(25)),
#     Column('conditionname', String(100)),
#     Column('conditionlevel', String(25)),
#     Column('testreason', String(75)),
#     Column('testnote', String(1000)),
#     Column('medicineorconditionnote', String(1000)),
#     Column('sublist', String(75)),
#     Column('medicine', String(100)),
#     Column('conditionnotefromusestable', String(250)),
#     Column('medicineusesgeneralnote', String(250)),
#     Column('categories', String(200)),
#     Column('lancet_gbd', String(3)),
#     Column('lancet_condition_tier', String(45)),
#     Column('ghana_condition_tier', String(25)),
#     Column('india_condition_tier', String(25)),
#     Column('nigeria_condition_tier', String(25)),
#     Column('kenya_condition_tier', String(25)),
#     Column('who_edl_indications', String(3)),
#     Column('test_name_short', String(50)),
#     Column('test_name_pretty', String(200)),
#     Column('clinical_service', String(100)),
#     Column('who_eml_v19', String(3)),
#     Column('who_eml_v20', String(3)),
#     Column('who_eml_v20_core', String(3)),
#     Column('who_eml_v20_complementary', String(3)),
#     Column('india_eml_2015_core', String(3)),
#     Column('ghana_nhis_2018', String(3)),
#     Column('ghana_eml_2010', String(3)),
#     Column('ghana_eml_2017', String(3)),
#     Column('ghana_eml_2017_level', String(5)),
#     Column('ghana_eml_2017_reimbursed', String(3)),
#     Column('notes', String(1000)),
#     Column('medicine_name', String(100)),
#     Column('representative', String(1)),
#     Column('preferred', String(1)),
#     Column('view_order', Integer),
#     Column('ghana_eml_2017_todo', String(4)),
#     Column('uid', Integer),
#     Column('enteredby', String(20)),
#     Column('ghana_nhis_2018_level', String(5)),
#     Column('kenya_eml_2016', String(3)),
#     Column('kenya_eml_2016_level', String(3)),
#     Column('kenya_eml_2016_todo', String(12)),
#     Column('categories_combined', Text),
#     Column('who_edl_v2', String(3)),
#     Column('india_edl_v1_draft', String(3)),
#     Column('test_format', String(100)),
#     Column('specimen_type', String(50)),
#     Column('laboratory', String(100)),
#     Column('nigeria_eml_2016', String(3)),
#     Column('nigeria_eml_2016_level', String(25)),
#     Column('nigeria_eml_2016_todo', String(12)),
#     Column('nigeria_eml_2016_enteredby', String(20)),
#     Column('eml_cat_1', Text),
#     Column('india_edl_v1_sup_draft', String(3)),
#     Column('who_edl_v2_tier', String(45)),
#     Column('india_edl_v1', String(3)),
#     Column('india_edl_v1_tier', String(45)),
#     Column('user_edl', String(3)),
#     Column('nigeria_test_tier_capacity', String(45)),
#     Column('ghana_nhis', String(3)),
#     Column('ghana_nhis_reimbursement_usd', String(10)),
#     Column('lancet_test_tier_capacity', String(25)),
#     Column('who_edl_v2_condition', Text),
#     Column('test_format_lancet_tier', String(25)),
#     Column('test_format_lancet_include', String(3)),
#     Column('lancet_indication_exclude', String(10)),
#     Column('condition_name_lancet', String(100)),
#     Column('clinical_chemistry', Integer),
#     Column('higherpriority', String(3)),
#     Column('indonesia_eml_phc', String),
#     Column('indonesia_phc_conditions', String),
#     Column('indonesia_phc_exclude', String)
# )


# t_tableau3_t2_tjfs_join_pre = Table(
#     'tableau3_t2_tjfs_join_pre', metadata,
#     Column('testname', String(100)),
#     Column('category', String(25)),
#     Column('conditionname', String(100)),
#     Column('conditionlevel', String(25)),
#     Column('testreason', String(75)),
#     Column('testnote', String(1000)),
#     Column('medicineorconditionnote', String(1000)),
#     Column('sublist', String(75)),
#     Column('medicine', String(100)),
#     Column('conditionnotefromusestable', String(250)),
#     Column('medicineusesgeneralnote', String(250)),
#     Column('categories', String(200)),
#     Column('lancet_gbd', String(3)),
#     Column('lancet_condition_tier', String(45)),
#     Column('ghana_condition_tier', String(25)),
#     Column('india_condition_tier', String(25)),
#     Column('nigeria_condition_tier', String(25)),
#     Column('kenya_condition_tier', String(25)),
#     Column('who_edl_indications', String(3)),
#     Column('test_name_short', String(50)),
#     Column('test_name_pretty', String(200)),
#     Column('clinical_service', String(100)),
#     Column('who_eml_v19', String(3)),
#     Column('who_eml_v20', String(3)),
#     Column('who_eml_v20_core', String(3)),
#     Column('who_eml_v20_complementary', String(3)),
#     Column('india_eml_2015_core', String(3)),
#     Column('ghana_nhis_2018', String(3)),
#     Column('ghana_eml_2010', String(3)),
#     Column('ghana_eml_2017', String(3)),
#     Column('ghana_eml_2017_level', String(5)),
#     Column('ghana_eml_2017_reimbursed', String(3)),
#     Column('notes', String(1000)),
#     Column('medicine_name', String(100)),
#     Column('representative', String(1)),
#     Column('preferred', String(1)),
#     Column('view_order', Integer),
#     Column('ghana_eml_2017_todo', String(4)),
#     Column('uid', Integer),
#     Column('enteredby', String(20)),
#     Column('ghana_nhis_2018_level', String(5)),
#     Column('kenya_eml_2016', String(3)),
#     Column('kenya_eml_2016_level', String(3)),
#     Column('kenya_eml_2016_todo', String(12)),
#     Column('categories_combined', Text),
#     Column('who_edl_v2', String(3)),
#     Column('india_edl_v1_draft', String(3)),
#     Column('test_format', String(100)),
#     Column('specimen_type', String(50)),
#     Column('laboratory', String(100)),
#     Column('nigeria_eml_2016', String(3)),
#     Column('nigeria_eml_2016_level', String(25)),
#     Column('nigeria_eml_2016_todo', String(12)),
#     Column('nigeria_eml_2016_enteredby', String(20)),
#     Column('eml_cat_1', Text),
#     Column('india_edl_v1_sup_draft', String(3)),
#     Column('who_edl_v2_tier', String(45)),
#     Column('india_edl_v1', String(3)),
#     Column('india_edl_v1_tier', String(45)),
#     Column('user_edl', String(3)),
#     Column('nigeria_test_tier_capacity', String(45)),
#     Column('ghana_nhis', String(3)),
#     Column('ghana_nhis_reimbursement_usd', String(10)),
#     Column('lancet_test_tier_capacity', String(25)),
#     Column('lancet_tier', String(25)),
#     Column('test_format_lancet_include', String(3)),
#     Column('lancet_exclude', String(10))
# )


# t_tableau3_t2_tjfs_join_pre_edl_dashadmin = Table(
#     'tableau3_t2_tjfs_join_pre_edl_dashadmin', metadata,
#     Column('testname', String(100)),
#     Column('category', String(25)),
#     Column('conditionname', String(100)),
#     Column('conditionlevel', String(25)),
#     Column('testreason', String(75)),
#     Column('testnote', String(1000)),
#     Column('medicineorconditionnote', String(1000)),
#     Column('sublist', String(75)),
#     Column('medicine', String(100)),
#     Column('conditionnotefromusestable', String(250)),
#     Column('medicineusesgeneralnote', String(250)),
#     Column('categories', String(200)),
#     Column('lancet_gbd', String(3)),
#     Column('lancet_condition_tier', String(45)),
#     Column('ghana_condition_tier', String(25)),
#     Column('india_condition_tier', String(25)),
#     Column('nigeria_condition_tier', String(25)),
#     Column('kenya_condition_tier', String(25)),
#     Column('who_edl_indications', String(3)),
#     Column('test_name_short', String(50)),
#     Column('test_name_pretty', String(200)),
#     Column('clinical_service', String(100)),
#     Column('who_eml_v19', String(3)),
#     Column('who_eml_v20', String(3)),
#     Column('who_eml_v20_core', String(3)),
#     Column('who_eml_v20_complementary', String(3)),
#     Column('india_eml_2015_core', String(3)),
#     Column('ghana_nhis_2018', String(3)),
#     Column('ghana_eml_2010', String(3)),
#     Column('ghana_eml_2017', String(3)),
#     Column('ghana_eml_2017_level', String(5)),
#     Column('ghana_eml_2017_reimbursed', String(3)),
#     Column('notes', String(1000)),
#     Column('medicine_name', String(100)),
#     Column('representative', String(1)),
#     Column('preferred', String(1)),
#     Column('view_order', Integer),
#     Column('ghana_eml_2017_todo', String(4)),
#     Column('uid', Integer),
#     Column('enteredby', String(20)),
#     Column('ghana_nhis_2018_level', String(5)),
#     Column('kenya_eml_2016', String(3)),
#     Column('kenya_eml_2016_level', String(3)),
#     Column('kenya_eml_2016_todo', String(12)),
#     Column('categories_combined', Text),
#     Column('who_edl_v2', String(3)),
#     Column('india_edl_v1_draft', String(3)),
#     Column('test_format', String(100)),
#     Column('specimen_type', String(50)),
#     Column('laboratory', String(100)),
#     Column('nigeria_eml_2016', String(3)),
#     Column('nigeria_eml_2016_level', String(25)),
#     Column('nigeria_eml_2016_todo', String(12)),
#     Column('nigeria_eml_2016_enteredby', String(20)),
#     Column('eml_cat_1', Text),
#     Column('india_edl_v1_sup_draft', String(3)),
#     Column('who_edl_v2_tier', String(45)),
#     Column('india_edl_v1', String(3)),
#     Column('india_edl_v1_tier', String(45)),
#     Column('user_edl', String(3)),
#     Column('nigeria_test_tier_capacity', String(45)),
#     Column('ghana_nhis', String(3)),
#     Column('ghana_nhis_reimbursement_usd', String(10)),
#     Column('lancet_test_tier_capacity', String(25)),
#     Column('lancet_tier', String(25)),
#     Column('test_format_lancet_include', String(3)),
#     Column('lancet_exclude', String(10)),
#     Column('indonesia_eml_phc', String)
# )


# t_tableau_cs_tcmj_join = Table(
#     'tableau_cs_tcmj_join', metadata,
#     Column('testname', String(100)),
#     Column('category', String(25)),
#     Column('conditionname', String(100)),
#     Column('testreason', String(75)),
#     Column('testnote', String(1000)),
#     Column('medicineorconditionnote', String(1000)),
#     Column('sublist', String(75)),
#     Column('medicine', String(100)),
#     Column('conditionnotefromusestable', String(250)),
#     Column('medicineusesgeneralnote', String(250)),
#     Column('categories', String(200)),
#     Column('ghana_condition_tier', String(25)),
#     Column('india_condition_tier', String(25)),
#     Column('nigeria_condition_tier', String(25)),
#     Column('kenya_condition_tier', String(25)),
#     Column('who_edl_indications', String(3)),
#     Column('test_name_short', String(50)),
#     Column('test_name_pretty', String(200)),
#     Column('clinical_service', String(100)),
#     Column('laboratory', String(100)),
#     Column('lancet_gbd', String(3)),
#     Column('lancet_condition_tier', String(45))
# )


# t_tableau_cs_tcmj_join_v1 = Table(
#     'tableau_cs_tcmj_join_v1', metadata,
#     Column('testname', String(100)),
#     Column('category', String(25)),
#     Column('conditionname', String(100)),
#     Column('conditionlevel', String(25)),
#     Column('testreason', String(75)),
#     Column('testnote', String(1000)),
#     Column('medicineorconditionnote', String(1000)),
#     Column('sublist', String(75)),
#     Column('medicine', String(100)),
#     Column('conditionnotefromusestable', String(250)),
#     Column('medicineusesgeneralnote', String(250)),
#     Column('categories', String(200)),
#     Column('lancet_gbd', String(3)),
#     Column('lancet_condition_tier', String(45)),
#     Column('ghana_condition_tier', String(25)),
#     Column('india_condition_tier', String(25)),
#     Column('nigeria_condition_tier', String(25)),
#     Column('kenya_condition_tier', String(25)),
#     Column('who_edl_indications', String(3)),
#     Column('test_name_short', String(50)),
#     Column('test_name_pretty', String(200)),
#     Column('clinical_service', String(100)),
#     Column('laboratory', String(100)),
#     Column('lancet_exclude', String(10))
# )


# class TestFormatsSpecimenTypesCopy(Base):
#     __tablename__ = 'test_formats_specimen_types_copy'

#     test_name = Column(String(100), nullable=False)
#     uid = Column(Integer, primary_key=True)
#     test_format = Column(String(100), nullable=False)
#     specimen_type = Column(String(50), nullable=False)


# class TestFormatsSpecimenTypesCopy2(Base):
#     __tablename__ = 'test_formats_specimen_types_copy2'

#     test_name = Column(String(100), nullable=False)
#     test_format = Column(String(100))
#     specimen_type = Column(String(50))
#     uid = Column(Integer, primary_key=True)


# t_test_formats_specimen_types_new = Table(
#     'test_formats_specimen_types_new', metadata,
#     Column('test_name', String(100)),
#     Column('test_format', String(100)),
#     Column('specimen_type', String(50))
# )


# t_test_indications_condition_related_join = Table(
#     'test_indications_condition_related_join', metadata,
#     Column('testname', String(100)),
#     Column('category', String(25)),
#     Column('conditionname', String(100)),
#     Column('testreason', String(75)),
#     Column('testnote', String(1000)),
#     Column('medicineorconditionnote', String(1000)),
#     Column('sublist', String(75)),
#     Column('medicine', String(100)),
#     Column('conditionnotefromusestable', String(250)),
#     Column('medicineusesgeneralnote', String(250)),
#     Column('categories', String(200)),
#     Column('ghana_condition_tier', String(25)),
#     Column('india_condition_tier', String(25)),
#     Column('nigeria_condition_tier', String(25)),
#     Column('kenya_condition_tier', String(25)),
#     Column('who_edl_indications', String(3)),
#     Column('test_name_short', String(50)),
#     Column('test_name_pretty', String(200)),
#     Column('laboratory', String(100)),
#     Column('lancet_gbd', String(3)),
#     Column('lancet_condition_tier', String(45)),
#     Column('condition_level', String(25))
# )


# t_test_indications_condition_related_join_v1 = Table(
#     'test_indications_condition_related_join_v1', metadata,
#     Column('testname', String(100)),
#     Column('category', String(25)),
#     Column('conditionname', String(100)),
#     Column('conditionlevel', String(25)),
#     Column('testreason', String(75)),
#     Column('testnote', String(1000)),
#     Column('medicineorconditionnote', String(1000)),
#     Column('sublist', String(75)),
#     Column('medicine', String(100)),
#     Column('conditionnotefromusestable', String(250)),
#     Column('medicineusesgeneralnote', String(250)),
#     Column('categories', String(200)),
#     Column('lancet_gbd', String(3)),
#     Column('lancet_condition_tier', String(45)),
#     Column('ghana_condition_tier', String(25)),
#     Column('india_condition_tier', String(25)),
#     Column('nigeria_condition_tier', String(25)),
#     Column('kenya_condition_tier', String(25)),
#     Column('who_edl_indications', String(3)),
#     Column('test_name_short', String(50)),
#     Column('test_name_pretty', String(200)),
#     Column('laboratory', String(100)),
#     Column('lancet_exclude', String(10))
# )


# t_test_indications_condition_related_with_name = Table(
#     'test_indications_condition_related_with_name', metadata,
#     Column('test_name', String(100)),
#     Column('test_note_about_condition', String(1000)),
#     Column('condition_name', String(100)),
#     Column('test_reason', String(75)),
#     Column('test_indication_note', String(1000)),
#     Column('sublists_who', String(75)),
#     Column('sublists_india_2015', String(75)),
#     Column('sublists_ghana_2017', String(75)),
#     Column('who_edl_indications', String(3)),
#     Column('uid', Integer),
#     Column('sublists_ghana_nhis_2018', String(75)),
#     Column('sublists_condition_related', String(75)),
#     Column('sublists_kenya_2016', String(75)),
#     Column('test_name_short', String(50)),
#     Column('test_name_pretty', String(200)),
#     Column('laboratory', String(100)),
#     Column('condition_level', String(25)),
#     Column('lancet_exclude', String(10))
# )


# t_test_indications_medicine_related_join = Table(
#     'test_indications_medicine_related_join', metadata,
#     Column('testname', String(100)),
#     Column('category', String(25)),
#     Column('conditionname', String(100)),
#     Column('testreason', String(75)),
#     Column('testnote', String(1000)),
#     Column('medicineorconditionnote', String(1000)),
#     Column('sublist', String(75)),
#     Column('medicine', String(100)),
#     Column('conditionnotefromusestable', String(250)),
#     Column('medicineusesgeneralnote', String(250)),
#     Column('categories', String(200)),
#     Column('ghana_condition_tier', String(25)),
#     Column('india_condition_tier', String(25)),
#     Column('nigeria_condition_tier', String(25)),
#     Column('kenya_condition_tier', String(25)),
#     Column('who_edl_indications', String(3)),
#     Column('test_name_short', String(50)),
#     Column('test_name_pretty', String(200)),
#     Column('laboratory', String(100)),
#     Column('lancet_gbd', String(3)),
#     Column('lancet_condition_tier', String(45)),
#     Column('condition_level', String(25))
# )


# t_test_indications_medicine_related_join_v1 = Table(
#     'test_indications_medicine_related_join_v1', metadata,
#     Column('testname', String(100)),
#     Column('category', String(25)),
#     Column('conditionname', String(100)),
#     Column('conditionlevel', String(25)),
#     Column('testreason', String(75)),
#     Column('testnote', String(1000)),
#     Column('medicineorconditionnote', String(1000)),
#     Column('sublist', String(75)),
#     Column('medicine', String(100)),
#     Column('conditionnotefromusestable', String(250)),
#     Column('medicineusesgeneralnote', String(250)),
#     Column('categories', String(200)),
#     Column('lancet_gbd', String(3)),
#     Column('lancet_condition_tier', String(45)),
#     Column('ghana_condition_tier', String(25)),
#     Column('india_condition_tier', String(25)),
#     Column('nigeria_condition_tier', String(25)),
#     Column('kenya_condition_tier', String(25)),
#     Column('who_edl_indications', String(3)),
#     Column('test_name_short', String(50)),
#     Column('test_name_pretty', String(200)),
#     Column('laboratory', String(100)),
#     Column('lancet_exclude', String(10))
# )


# t_test_indications_medicine_related_with_name = Table(
#     'test_indications_medicine_related_with_name', metadata,
#     Column('medicine_name', String(100)),
#     Column('test_name', String(100)),
#     Column('test_reason_medicine_related', String(75)),
#     Column('test_note', String(1000)),
#     Column('medicine_note', String(1000)),
#     Column('sublist_medicine_related', String(75)),
#     Column('who_edl_indications', String(3)),
#     Column('uid', Integer),
#     Column('test_name_short', String(50)),
#     Column('test_name_pretty', String(200)),
#     Column('laboratory', String(100)),
#     Column('lancet_exclude', String(10))
# )


# class TestReasonsConditionRelated(Base):
#     __tablename__ = 'test_reasons_condition_related'

#     test_reason_condition_related = Column(String(20), primary_key=True)


# class TestReasonsMedicineRelated(Base):
#     __tablename__ = 'test_reasons_medicine_related'

#     test_reason_medicine_related = Column(String(20), primary_key=True)


# t_tests_conditions_meds_join = Table(
#     'tests_conditions_meds_join', metadata,
#     Column('testname', String(100)),
#     Column('category', String(25)),
#     Column('conditionname', String(100)),
#     Column('testreason', String(75)),
#     Column('testnote', String(1000)),
#     Column('medicineorconditionnote', String(1000)),
#     Column('sublist', String(75)),
#     Column('medicine', String(100)),
#     Column('conditionnotefromusestable', String(250)),
#     Column('medicineusesgeneralnote', String(250)),
#     Column('categories', String(200)),
#     Column('ghana_condition_tier', String(25)),
#     Column('india_condition_tier', String(25)),
#     Column('nigeria_condition_tier', String(25)),
#     Column('kenya_condition_tier', String(25)),
#     Column('who_edl_indications', String(3)),
#     Column('test_name_short', String(50)),
#     Column('test_name_pretty', String(200)),
#     Column('laboratory', String(100)),
#     Column('lancet_gbd', String(3)),
#     Column('lancet_condition_tier', String(45))
# )


# t_tests_conditions_meds_join_v1 = Table(
#     'tests_conditions_meds_join_v1', metadata,
#     Column('testname', String(100)),
#     Column('category', String(25)),
#     Column('conditionname', String(100)),
#     Column('conditionlevel', String(25)),
#     Column('testreason', String(75)),
#     Column('testnote', String(1000)),
#     Column('medicineorconditionnote', String(1000)),
#     Column('sublist', String(75)),
#     Column('medicine', String(100)),
#     Column('conditionnotefromusestable', String(250)),
#     Column('medicineusesgeneralnote', String(250)),
#     Column('categories', String(200)),
#     Column('lancet_gbd', String(3)),
#     Column('lancet_condition_tier', String(45)),
#     Column('ghana_condition_tier', String(25)),
#     Column('india_condition_tier', String(25)),
#     Column('nigeria_condition_tier', String(25)),
#     Column('kenya_condition_tier', String(25)),
#     Column('who_edl_indications', String(3)),
#     Column('test_name_short', String(50)),
#     Column('test_name_pretty', String(200)),
#     Column('laboratory', String(100)),
#     Column('lancet_exclude', String(10))
# )


# t_tests_joined_format_specimens = Table(
#     'tests_joined_format_specimens', metadata,
#     Column('test_name', String(100)),
#     Column('who_edl_v2', String(3)),
#     Column('india_edl_v1_draft', String(3)),
#     Column('test_format', String(100)),
#     Column('specimen_type', String(50)),
#     Column('india_edl_v1_sup_draft', String(3)),
#     Column('who_edl_v2_tier', String(45)),
#     Column('india_edl_v1', String(3)),
#     Column('india_edl_v1_tier', String(45)),
#     Column('nigeria_test_tier_capacity', String(45)),
#     Column('ghana_nhis', String(3)),
#     Column('ghana_nhis_reimbursement_usd', String(10)),
#     Column('lancet_test_tier_capacity', String(25))
# )


# t_tests_specimens = Table(
#     'tests_specimens', metadata,
#     Column('test_name', String(100)),
#     Column('test_name_pretty', String(200)),
#     Column('test_name_short', String(50)),
#     Column('laboratory', String(100)),
#     Column('clinical_chemistry', Integer),
#     Column('us_lab_upper_peninsula1', Integer),
#     Column('us_lab_upper_peninsula2', Integer),
#     Column('india_free_diagnostics', Integer),
#     Column('who_edl_v1', String(3)),
#     Column('india_edl_v1_draft', String(3)),
#     Column('india_edl_v1_sup_draft', String(3)),
#     Column('who_edl_v2', String(3)),
#     Column('uid', Integer),
#     Column('test_format', String(100)),
#     Column('specimen_type', String(50))
# )


# t_tests_with_model_tiers_count_v1 = Table(
#     'tests_with_model_tiers_count_v1', metadata,
#     Column('test_name', String(100)),
#     Column('col1', Integer),
#     Column('col2', Integer),
#     Column('col3', Integer),
#     Column('col4', Integer),
#     Column('col5', Integer),
#     Column('col6', Integer)
# )


# t_tests_with_model_tiers_v1 = Table(
#     'tests_with_model_tiers_v1', metadata,
#     Column('test_name', String(100)),
#     Column('test_name_pretty', String(200)),
#     Column('test_name_short', String(50)),
#     Column('laboratory', String(100)),
#     Column('who_edl_v2', String(3)),
#     Column('who_edl_v2_tier', String(45)),
#     Column('who_edl_v2_tier_model', String(45)),
#     Column('who_edl_v2_tier_model_value', Numeric(10, 0)),
#     Column('india_edl_v1', String(3)),
#     Column('india_edl_v1_tier', String(45)),
#     Column('india_edl_v1_tier_model', String(45)),
#     Column('india_edl_v1_tier_model_value', Numeric(10, 0)),
#     Column('ethiopia_chai', String(3)),
#     Column('ethiopia_chai_tier', String(45)),
#     Column('ethiopia_chai_tier_model', String(45)),
#     Column('ethiopia_chai_tier_model_value', Numeric(10, 0)),
#     Column('ghana_moh', String(3)),
#     Column('ghana_moh_tier', String(45)),
#     Column('ghana_moh_tier_model', String(45)),
#     Column('ghana_moh_tier_model_value', Numeric(10, 0)),
#     Column('ethiopia_standards', String(3)),
#     Column('ethiopia_standards_tier', String(45)),
#     Column('ethiopia_standards_tier_model', String(45)),
#     Column('ethiopia_standards_tier_model_value', Numeric(10, 0)),
#     Column('rwanda_ministerial_order', String(3)),
#     Column('rwanda_ministerial_order_tier', String(45)),
#     Column('rwanda_ministerial_order_tier_model', String(45)),
#     Column('rwanda_ministerial_order_tier_model_value', Numeric(10, 0)),
#     Column('lancet_package', String(3)),
#     Column('lancet_package_tier', String(25)),
#     Column('lancet_package_tier_model', String(45)),
#     Column('lancet_package_tier_model_value', Numeric(10, 0))
# )


# t_tests_with_model_tiers_with_counts = Table(
#     'tests_with_model_tiers_with_counts', metadata,
#     Column('test_name', String(100)),
#     Column('test_name_pretty', String(200)),
#     Column('test_name_short', String(50)),
#     Column('laboratory', String(100)),
#     Column('lists_with_tests', Integer),
#     Column('avg_tier_value', Numeric),
#     Column('who_edl_v2', String(3)),
#     Column('who_edl_v2_tier', String(45)),
#     Column('who_edl_v2_tier_model', String(45)),
#     Column('who_edl_v2_tier_model_value', Numeric(10, 0)),
#     Column('india_edl_v1', String(3)),
#     Column('india_edl_v1_tier', String(45)),
#     Column('india_edl_v1_tier_model', String(45)),
#     Column('india_edl_v1_tier_model_value', Numeric(10, 0)),
#     Column('ethiopia_chai', String(3)),
#     Column('ethiopia_chai_tier', String(45)),
#     Column('ethiopia_chai_tier_model', String(45)),
#     Column('ethiopia_chai_tier_model_value', Numeric(10, 0)),
#     Column('ghana_moh', String(3)),
#     Column('ghana_moh_tier', String(45)),
#     Column('ghana_moh_tier_model', String(45)),
#     Column('ghana_moh_tier_model_value', Numeric(10, 0)),
#     Column('ethiopia_standards', String(3)),
#     Column('ethiopia_standards_tier', String(45)),
#     Column('ethiopia_standards_tier_model', String(45)),
#     Column('ethiopia_standards_tier_model_value', Numeric(10, 0)),
#     Column('rwanda_ministerial_order', String(3)),
#     Column('rwanda_ministerial_order_tier', String(45)),
#     Column('rwanda_ministerial_order_tier_model', String(45)),
#     Column('rwanda_ministerial_order_tier_model_value', Numeric(10, 0)),
#     Column('lancet_package', String(3)),
#     Column('lancet_package_tier', String(25)),
#     Column('lancet_package_tier_model', String(45)),
#     Column('lancet_package_tier_model_value', Numeric(10, 0))
# )


# class TiersModel(Base):
#     __tablename__ = 'tiers_model'

#     tier = Column(String(45), primary_key=True)
#     tier_value = Column(Numeric(10, 0))


# t_user_edl = Table(
#     'user_edl', metadata,
#     Column('test_name_pretty', String(200)),
#     Column('lad_edl', String(3))
# )


# t_who_edl_conditions = Table(
#     'who_edl_conditions', metadata,
#     Column('conditionname', String(100)),
#     Column('who_edl_v2_condition', Text)
# )


# t_who_edl_conditions_clean = Table(
#     'who_edl_conditions_clean', metadata,
#     Column('conditionname', String(100)),
#     Column('who_edl_v2_condition', Text)
# )


# t_who_edl_v2_tiers_with_values = Table(
#     'who_edl_v2_tiers_with_values', metadata,
#     Column('tier', String(45)),
#     Column('tier_model', String(45)),
#     Column('tier_value', Numeric(10, 0))
# )


# class Condition(Base):
#     __tablename__ = 'conditions'

#     condition_name = Column(String(100), primary_key=True)
#     condition_name_short = Column(String(50))
#     ghana_condition_tier = Column(String(25))
#     india_condition_tier = Column(String(25))
#     nigeria_condition_tier = Column(String(25))
#     kenya_condition_tier = Column(String(25))
#     lancet_condition_tier = Column(ForeignKey('lancet_condition_tiers.tier'))
#     lancet_gbd = Column(String(3))
#     condition_level = Column(String(25))
#     condition_name_lancet = Column(String(100))
#     indonesia_phc_conditions = Column(String)
#     who_amr_conditions = Column(String)

#     lancet_condition_tier1 = relationship('LancetConditionTier')


# class Eml(Base):
#     __tablename__ = 'emls'

#     who_eml_v19 = Column(String(3))
#     who_eml_v20 = Column(String(3))
#     who_eml_v20_core = Column(String(3))
#     who_eml_v20_complementary = Column(String(3))
#     india_eml_2015_core = Column(String(3))
#     ghana_nhis_2018 = Column(String(3))
#     ghana_eml_2010 = Column(String(3))
#     ghana_eml_2017 = Column(String(3))
#     ghana_eml_2017_level = Column(ForeignKey('ghana_eml_tiers.ghana_eml_tier'))
#     ghana_eml_2017_reimbursed = Column(String(3))
#     notes = Column(String(1000))
#     medicine_name = Column(ForeignKey('medicines.medicine_name'), nullable=False)
#     representative = Column(String(1))
#     preferred = Column(String(1))
#     category1 = Column(ForeignKey('eml_category_1.eml_category1_name'))
#     category2 = Column(ForeignKey('eml_category_2.eml_category_2_name'))
#     category3 = Column(ForeignKey('eml_category_3.eml_category_3_name'))
#     category4 = Column(ForeignKey('eml_category_4.eml_category_4_name'))
#     category5 = Column(ForeignKey('eml_category_5.eml_category_5_name'))
#     category6 = Column(ForeignKey('eml_category_6.eml_category_6_name'))
#     view_order = Column(Integer)
#     ghana_eml_2017_todo = Column(String(4))
#     uid = Column(Integer, primary_key=True)
#     enteredby = Column(String(20))
#     ghana_nhis_2018_level = Column(String(5))
#     kenya_eml_2016 = Column(String(3))
#     kenya_eml_2016_level = Column(String(3))
#     kenya_eml_2016_todo = Column(String(12))
#     nigeria_eml_2016 = Column(String(3))
#     nigeria_eml_2016_level = Column(ForeignKey('nigeria_eml_tiers.nigeria_eml_tier'))
#     nigeria_eml_2016_todo = Column(String(12))
#     nigeria_eml_2016_enteredby = Column(String(20))
#     india_eml_2015_level = Column(ForeignKey('india_eml_tiers.india_eml_tier'))
#     indonesia_eml_phc = Column(String, comment='From FIND')

#     eml_category_1 = relationship('EmlCategory1')
#     eml_category_2 = relationship('EmlCategory2')
#     eml_category_3 = relationship('EmlCategory3')
#     eml_category_4 = relationship('EmlCategory4')
#     eml_category_5 = relationship('EmlCategory5')
#     eml_category_6 = relationship('EmlCategory6')
#     ghana_eml_tier = relationship('GhanaEmlTier')
#     india_eml_tier = relationship('IndiaEmlTier')
#     medicine = relationship('Medicine')
#     nigeria_eml_tier = relationship('NigeriaEmlTier')


# class EthiopiaChaiTier(Base):
#     __tablename__ = 'ethiopia_chai_tiers'

#     tier = Column(String(25), primary_key=True)
#     tier_model = Column(ForeignKey('tiers_model.tier'))

#     tiers_model = relationship('TiersModel')


# class EthiopiaStandardsTier(Base):
#     __tablename__ = 'ethiopia_standards_tiers'

#     tier = Column(String(45), primary_key=True)
#     tier_model = Column(ForeignKey('tiers_model.tier'))

#     tiers_model = relationship('TiersModel')


# class GhanaMohTier(Base):
#     __tablename__ = 'ghana_moh_tiers'

#     tier = Column(String(25), primary_key=True)
#     tier_model = Column(ForeignKey('tiers_model.tier'))

#     tiers_model = relationship('TiersModel')


# class IndiaEdlTier(Base):
#     __tablename__ = 'india_edl_tiers'

#     tier = Column(String(45), primary_key=True)
#     tier_model = Column(ForeignKey('tiers_model.tier'))

#     tiers_model = relationship('TiersModel')


# class LancetPackageTier(Base):
#     __tablename__ = 'lancet_package_tiers'

#     tier = Column(String(25), primary_key=True)
#     tier_model = Column(ForeignKey('tiers_model.tier'))

#     tiers_model = relationship('TiersModel')


# class RwandaMinisterialOrderTier(Base):
#     __tablename__ = 'rwanda_ministerial_order_tiers'

#     tier = Column(String(45), primary_key=True)
#     tier_model = Column(ForeignKey('tiers_model.tier'))

#     tiers_model = relationship('TiersModel')


# class TestFormat(Base):
#     __tablename__ = 'test_formats'

#     test_format = Column(String(50), primary_key=True)
#     lancet_tier = Column(ForeignKey('lancet_condition_tiers.tier'))
#     test_format_lancet_include = Column(String(3))

#     lancet_condition_tier = relationship('LancetConditionTier')


# class WhoEdlV2Tier(Base):
#     __tablename__ = 'who_edl_v2_tiers'

#     tier = Column(String(45), primary_key=True)
#     tier_model = Column(ForeignKey('tiers_model.tier'))

#     tiers_model = relationship('TiersModel')


# t_condition_services = Table(
#     'condition_services', metadata,
#     Column('condition_name', ForeignKey('conditions.condition_name'), primary_key=True),
#     Column('clinical_service', ForeignKey('clinical_services.clinical_service'), nullable=False)
# )


# class ConditionsTier(Base):
#     __tablename__ = 'conditions_tiers'

#     condition_name = Column(ForeignKey('conditions.condition_name'), nullable=False)
#     ghana_condition_tier = Column(String(25))
#     india_condition_tier = Column(String(25))
#     nigeria_condition_tier = Column(String(25))
#     kenya_condition_tier = Column(String(25))
#     lancet_condition_tier = Column(ForeignKey('lancet_condition_tiers.tier'))
#     condition_level = Column(ForeignKey('condition_levels.condition_level'))
#     uid = Column(Integer, primary_key=True)

#     condition_level1 = relationship('ConditionLevel')
#     condition = relationship('Condition')
#     lancet_condition_tier1 = relationship('LancetConditionTier')


# class MedicineIndication(Base):
#     __tablename__ = 'medicine_indications'

#     medicine_name = Column(ForeignKey('medicines.medicine_name'))
#     medicine_note = Column(String(250))
#     condition_name = Column(ForeignKey('conditions.condition_name'))
#     condition_note = Column(String(250))
#     condition_number = Column(String(5))
#     who_eml_indication = Column(String(1))
#     india_eml_2015_indication = Column(String(1))
#     india_eml_2015_indication_only = Column(String(1))
#     ghana_eml_2017_indication = Column(String(3))
#     uid = Column(Integer, primary_key=True)
#     medicine_category = Column(String(200))
#     medicine_category_todo = Column(String(10))
#     condition_level = Column(ForeignKey('condition_levels.condition_level'))

#     condition_level1 = relationship('ConditionLevel')
#     condition = relationship('Condition')
#     medicine = relationship('Medicine')


# class Test(Base):
#     __tablename__ = 'tests'

#     test_name = Column(String(100), primary_key=True)
#     test_name_pretty = Column(String(200))
#     test_name_short = Column(String(50))
#     laboratory = Column(ForeignKey('laboratory_sections.lab_section'))
#     clinical_chemistry = Column(Integer)
#     us_lab_upper_peninsula1 = Column(Integer)
#     us_lab_upper_peninsula2 = Column(Integer)
#     india_free_diagnostics = Column(Integer)
#     who_edl_v1 = Column(String(3))
#     india_edl_v1_draft = Column(String(3))
#     india_edl_v1_sup_draft = Column(String(3))
#     who_edl_v2 = Column(String(3))
#     who_edl_v2_tier = Column(ForeignKey('who_edl_v2_tiers.tier'))
#     india_edl_v1 = Column(String(3))
#     india_edl_v1_tier = Column(ForeignKey('india_edl_tiers.tier'))
#     nigeria_test_tier_capacity = Column(ForeignKey('nigeria_eml_tiers.nigeria_eml_tier'), comment='This is the lowest tier that has the infrastructural capacity to potentially perform the test')
#     ethiopia_chai = Column(String(3))
#     ethiopia_chai_tier = Column(ForeignKey('ethiopia_chai_tiers.tier'))
#     ghana_nhis = Column(String(3))
#     ghana_nhis_reimbursement_usd = Column(String(10))
#     ghana_moh = Column(String(3))
#     ghana_moh_tier = Column(String(45))
#     kenya_countyhospitals = Column(String(3))
#     kenya_countyhospital_price_usd = Column(String(10))
#     ethiopia_standards = Column(String(3))
#     ethiopia_standards_tier = Column(ForeignKey('ethiopia_standards_tiers.tier'))
#     rwanda_ministerial_order = Column(String(3))
#     rwanda_ministerial_order_tier = Column(ForeignKey('rwanda_ministerial_order_tiers.tier'))
#     lancet_test_tier_capacity = Column(ForeignKey('lancet_condition_tiers.tier'))
#     test_name_lancet = Column(String(200))
#     lancet_package = Column(String(3))
#     higherpriority = Column(String(3))
#     lancet_package_tier = Column(ForeignKey('lancet_package_tiers.tier'))
#     indonesia_phc_exclude = Column(String)

#     ethiopia_chai_tier1 = relationship('EthiopiaChaiTier')
#     ethiopia_standards_tier1 = relationship('EthiopiaStandardsTier')
#     india_edl_tier = relationship('IndiaEdlTier')
#     laboratory_section = relationship('LaboratorySection')
#     lancet_package_tier1 = relationship('LancetPackageTier')
#     lancet_condition_tier = relationship('LancetConditionTier')
#     nigeria_eml_tier = relationship('NigeriaEmlTier')
#     rwanda_ministerial_order_tier1 = relationship('RwandaMinisterialOrderTier')
#     who_edl_v2_tier1 = relationship('WhoEdlV2Tier')


# class TestFormatsSpecimenType(Base):
#     __tablename__ = 'test_formats_specimen_types'

#     test_name = Column(ForeignKey('tests.test_name'), nullable=False)
#     uid = Column(Integer, primary_key=True)
#     test_format = Column(ForeignKey('test_formats.test_format'))
#     specimen_type = Column(ForeignKey('specimen_types.specimen_type'))

#     specimen_type1 = relationship('SpecimenType')
#     test_format1 = relationship('TestFormat')
#     test = relationship('Test')


# class TestIndicationsConditionRelated(Base):
#     __tablename__ = 'test_indications_condition_related'

#     test_name = Column(ForeignKey('tests.test_name'))
#     test_note_about_condition = Column(String(1000))
#     condition_name = Column(ForeignKey('conditions.condition_name'))
#     test_reason = Column(ForeignKey('test_reasons_condition_related.test_reason_condition_related'))
#     test_indication_note = Column(String(1000))
#     sublists_who = Column(ForeignKey('sublist_categories_condition_related.sublist_category'))
#     sublists_india_2015 = Column(ForeignKey('sublist_categories_condition_related.sublist_category'))
#     sublists_ghana_2017 = Column(ForeignKey('sublist_categories_condition_related.sublist_category'))
#     who_edl_indications = Column(String(3))
#     uid = Column(Integer, primary_key=True)
#     sublists_ghana_nhis_2018 = Column(String(75))
#     sublists_condition_related = Column(String(75), nullable=False)
#     sublists_kenya_2016 = Column(String(75))
#     condition_level = Column(String(25))
#     lancet_exclude = Column(String(10))

#     condition = relationship('Condition')
#     sublist_categories_condition_related = relationship('SublistCategoriesConditionRelated', primaryjoin='TestIndicationsConditionRelated.sublists_ghana_2017 == SublistCategoriesConditionRelated.sublist_category')
#     sublist_categories_condition_related1 = relationship('SublistCategoriesConditionRelated', primaryjoin='TestIndicationsConditionRelated.sublists_india_2015 == SublistCategoriesConditionRelated.sublist_category')
#     sublist_categories_condition_related2 = relationship('SublistCategoriesConditionRelated', primaryjoin='TestIndicationsConditionRelated.sublists_who == SublistCategoriesConditionRelated.sublist_category')
#     test = relationship('Test')
#     test_reasons_condition_related = relationship('TestReasonsConditionRelated')


# class TestIndicationsMedicineRelated(Base):
#     __tablename__ = 'test_indications_medicine_related'

#     medicine_name = Column(ForeignKey('medicines.medicine_name'))
#     test_name = Column(ForeignKey('tests.test_name'))
#     test_reason_medicine_related = Column(ForeignKey('test_reasons_medicine_related.test_reason_medicine_related'))
#     test_note = Column(String(1000))
#     medicine_note = Column(String(1000))
#     sublist_medicine_related = Column(ForeignKey('sublist_categories_medicine_related.sublist_categories'), ForeignKey('sublist_categories_medicine_related.sublist_categories'))
#     who_edl_indications = Column(String(3))
#     uid = Column(Integer, primary_key=True)
#     lancet_exclude = Column(String(10))

#     medicine = relationship('Medicine')
#     sublist_categories_medicine_related = relationship('SublistCategoriesMedicineRelated', primaryjoin='TestIndicationsMedicineRelated.sublist_medicine_related == SublistCategoriesMedicineRelated.sublist_categories')
#     sublist_categories_medicine_related1 = relationship('SublistCategoriesMedicineRelated', primaryjoin='TestIndicationsMedicineRelated.sublist_medicine_related == SublistCategoriesMedicineRelated.sublist_categories')
#     test = relationship('Test')
#     test_reasons_medicine_related = relationship('TestReasonsMedicineRelated')
