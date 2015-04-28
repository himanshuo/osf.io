NODE_SUBSCRIPTIONS_AVAILABLE = {
    'comments': 'Comments Added'
}

USER_SUBSCRIPTIONS_AVAILABLE = {
    'comment_replies': 'Replies to your comments'
}

# Note: the python value None mean inherit from parent
NOTIFICATION_TYPES = {
    'email_transactional': 'Email when a change occurs',
    'email_digest': 'Daily email digest of all changes to this project',
    'none': 'None'
}

# Formatted file provider names for notification emails
PROVIDERS = {
    'osfstorage': 'OSF Storage',
    'box': 'Box',
    'dataverse': 'Dataverse',
    'dropbox': 'Dropbox',
    'figshare': 'figshare',
    'github': 'GitHub',
    'googledrive': 'Google Drive',
    's3': 'Amazon S3'
}