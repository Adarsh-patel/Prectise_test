{
    'name':'prectise',
    'version':'1.0',
    'summary':'For Prectise',
    'depends':['purchase','sale','sale_management','hr'],
    'data':[
        'security/sale_security.xml',
        'views/sample_view.xml',
        'report/inherit_purchse_order_report.xml',
        'data/ir_sequence_data.xml',

    ],
    'installable':True,
    'auto_install':False,
    'application':False,

}