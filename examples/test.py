a = """
, vcc_coms_raw, aio_acceptance_records          , 
, vcc_coms_raw, aio_acceptance_records_detail   , 
, vcc_coms_raw, aio_config_service              , 
, vcc_coms_raw, aio_contract                    , 
, vcc_coms_raw, aio_contract_20190412           , 
, vcc_coms_raw, aio_contract_detail             , 
, vcc_coms_raw, aio_customer                    , 
, vcc_coms_raw, aio_goods_price                 , 
, vcc_coms_raw, aio_location_user               , 
, vcc_coms_raw, aio_package                     , 
, vcc_coms_raw, aio_package_detail              , 
, vcc_coms_raw, aio_package_goods               , 
, vcc_coms_raw, aio_package_goods_add           , 
, vcc_coms_raw, asset_manage_request_entity     , 
, vcc_coms_raw, asset_management_request        , 
, vcc_coms_raw, asset_repair_report             , 
, vcc_coms_raw, assign_handover                 , 
, vcc_coms_raw, chart_quantity_complete         , 
, vcc_coms_raw, chart_quantity_complete_acc     , 
, vcc_coms_raw, config_group_province           , 
, vcc_coms_raw, config_user_province            , 
, vcc_coms_raw, construction                    , 
, vcc_coms_raw, construction_acceptance_cert    , 
, vcc_coms_raw, construction_ctct               , 
, vcc_coms_raw, construction_merchandise        , 
, vcc_coms_raw, construction_return             , 
, vcc_coms_raw, construction_task               , 
, vcc_coms_raw, construction_task_20190518      , 
, vcc_coms_raw, construction_task_daily         , 
, vcc_coms_raw, contact_unit                    , 
, vcc_coms_raw, contact_unit_detail             , 
, vcc_coms_raw, contact_unit_detail_description , 
, vcc_coms_raw, contruction_land_handover_plan  , 
, vcc_coms_raw, detail_month_plan               , 
, vcc_coms_raw, dmpn_order                      , 
, vcc_coms_raw, goods_plan                      , 
, vcc_coms_raw, goods_plan_detail               , 
, vcc_coms_raw, issue                           , 
, vcc_coms_raw, issue_dicuss                    , 
, vcc_coms_raw, issue_history                   , 
, vcc_coms_raw, kcs_acceptance_report           , 
, vcc_coms_raw, kcs_check_rep_entity            , 
, vcc_coms_raw, kcs_check_report                , 
, vcc_coms_raw, kcs_check_req                   , 
, vcc_coms_raw, kcs_check_req_entity            , 
, vcc_coms_raw, kcs_check_tm                    , 
, vcc_coms_raw, kcs_config_alert                , 
, vcc_coms_raw, kcs_history                     , 
, vcc_coms_raw, kcs_quality_note                , 
, vcc_coms_raw, kcs_related_annex               , 
, vcc_coms_raw, kpi_log_mobile                  , 
, vcc_coms_raw, kpi_log_time_process            , 
, vcc_coms_raw, manage_data_outside_os          , 
, vcc_coms_raw, obstructed                      , 
, vcc_coms_raw, request_goods                   , 
, vcc_coms_raw, request_goods_detail            , 
, vcc_coms_raw, rp_bts                          , 
, vcc_coms_raw, rp_giacocot                     , 
, vcc_coms_raw, rp_hshc                         , 
, vcc_coms_raw, rp_quantity                     , 
, vcc_coms_raw, rp_revenue                      , 
, vcc_coms_raw, rp_station_complete             , 
, vcc_coms_raw, rp_station_complete_construction, 
, vcc_coms_raw, settlement_debt_a               , 
, vcc_coms_raw, shipment_tax                    , 
, vcc_coms_raw, sqln_explain_plan               , 
, vcc_coms_raw, st_transaction                  , 
, vcc_coms_raw, stock_trans_confirm             , 
, vcc_coms_raw, syn_stock_daily_import_export   , 
, vcc_coms_raw, syn_stock_daily_remain          , 
, vcc_coms_raw, syn_stock_daily_remain_erp      , 
, vcc_coms_raw, syn_stock_daily_report          , 
, vcc_coms_raw, syn_stock_total                 , 
, vcc_coms_raw, syn_stock_trans                 , 
, vcc_coms_raw, syn_stock_trans_detail          , 
, vcc_coms_raw, syn_stock_trans_detail_20190712 , 
, vcc_coms_raw, syn_stock_trans_detail_serial   , 
, vcc_coms_raw, tmpn_contract                   , 
, vcc_coms_raw, tmpn_finance                    , 
, vcc_coms_raw, tmpn_force_maintain             , 
, vcc_coms_raw, tmpn_force_new_bts              , 
, vcc_coms_raw, tmpn_force_new_line             , 
, vcc_coms_raw, tmpn_material                   , 
, vcc_coms_raw, tmpn_source                     , 
, vcc_coms_raw, tmpn_target                     , 
, vcc_coms_raw, tmpn_target_os                  , 
, vcc_coms_raw, total_month_plan                , 
, vcc_coms_raw, total_month_plan_os             , 
, vcc_coms_raw, user_holiday                    , 
, vcc_coms_raw, work_item                       , 
, vcc_coms_raw, work_item_20190921              , 
, vcc_coms_raw, work_item_gpon                  , 
, vcc_coms_raw, year_plan                       , 
, vcc_coms_raw, year_plan_detail                , 
, vcc_coms_raw, year_plan_detail_os             , 
, vcc_coms_raw, year_plan_detail_per_month      , 
, vcc_coms_raw, year_plan_os                    , 
"""

df = [[i for i in k.split(",")] for k in a.split("\n")]
for k in df:
    if k != "":
        a = [i.strip() for i in k if i.strip() != ""]
        if len(a) > 1:
            temp = "DROP TABLE %s.%s;" % (a[0], a[1])
            print(temp)
