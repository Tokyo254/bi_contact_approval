{
    'name': 'Contact Approval Access',
    'version': '17.0.0.1',
    'category': 'Contacts',
    'summary': 'Two-step approval workflow for contacts',
    'depends': ['base', 'contacts', 'mail'],
    'data': [
        'security/base_groups.xml',
        'views/res_partner_views.xml',
    ],
    'installable': True,
    'auto_install': False,
}
