"""Role permissions adapted from UES desktop v2.5.2; server-side authority."""
ALLOWED_TABLES = {'organizations','roles','permissions','users','profiles','memberships','invitations','contacts','contact_identities','channels','conversations','messages','message_attachments','leads','lead_activities','service_categories','services','pricing_rules','quotes','quote_items','quote_approvals','quote_acceptances','contracts','contract_milestones','projects','project_members','tasks','task_comments','team_availability','invoices','payments','expenses','agents','knowledge_documents','ai_conversation_runs','automation_rules','automation_runs','notifications','approvals','files','settings','activity_logs','webhook_events','integration_connections','client_portal_access'}
IDENTITY_TABLES = {'users','roles','permissions','memberships','invitations','profiles','activity_logs'}
PUBLIC_NAMES = {'id','username','email','role_code','is_owner','is_active','organization_id','last_login_at','created_at','updated_at'}
ROLE_READ = {
    'general_manager': {'organizations','contacts','contact_identities','channels','conversations','messages','message_attachments','leads','lead_activities','service_categories','services','pricing_rules','quotes','quote_items','quote_approvals','quote_acceptances','contracts','contract_milestones','projects','project_members','tasks','task_comments','team_availability','agents','knowledge_documents','ai_conversation_runs','automation_rules','notifications','approvals','files','activity_logs'},
    'sales_manager': {'organizations','contacts','contact_identities','channels','conversations','messages','message_attachments','leads','lead_activities','service_categories','services','pricing_rules','quotes','quote_items','quote_approvals','quote_acceptances','contracts','contract_milestones','notifications','approvals'},
    'sales_rep': {'organizations','contacts','contact_identities','channels','conversations','messages','message_attachments','leads','lead_activities','service_categories','services','pricing_rules','quotes','quote_items','notifications'},
    'academic_manager': {'organizations','contacts','service_categories','services','projects','project_members','tasks','task_comments','team_availability','knowledge_documents','files','notifications'},
    'academic_specialist': {'organizations','contacts','projects','project_members','tasks','task_comments','files','notifications'},
    'finance_manager': {'organizations','contacts','contracts','contract_milestones','invoices','payments','expenses','notifications','approvals'},
    'customer_support': {'organizations','contacts','contact_identities','channels','conversations','messages','message_attachments','leads','lead_activities','notifications'},
    'viewer': {'organizations'},
    'client': {'organizations','contacts','contracts','contract_milestones','projects','tasks','invoices','payments','files','client_portal_access','notifications'}
}
ROLE_WRITE = {
    'general_manager': {'contacts','leads','lead_activities','conversations','messages','projects','tasks','task_comments','project_members','team_availability','quotes','quote_items','files','notifications'},
    'sales_manager': {'contacts','contact_identities','leads','lead_activities','conversations','messages','quotes','quote_items','quote_approvals','quote_acceptances','notifications'},
    'sales_rep': {'contacts','contact_identities','leads','lead_activities','conversations','messages','quotes','quote_items','notifications'},
    'academic_manager': {'projects','tasks','task_comments','project_members','team_availability','files','notifications'},
    'academic_specialist': {'tasks','task_comments','notifications'},
    'finance_manager': {'invoices','expenses','notifications'},
    'customer_support': {'contacts','contact_identities','leads','lead_activities','conversations','messages','notifications'}
}
PROTECTED_WRITE = IDENTITY_TABLES | {'payments','integration_connections','webhook_events'}
