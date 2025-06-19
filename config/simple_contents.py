NORMAL = {
        'FIRST_LAUNCH': 'Un utilisateur de l\'équipe Management va être créé\nafin de pouvoir continuer.',
        'NO_CLIENT_WITHOUT_EVENT': 'Pas de client avec contrat sans évènement.',
        'UNKNOWN': 'Cette commande est inconnue.',
        'MAIN_MENU': ('Merci d\'entrer la commande correspondant à ce que vous souhaitez faire.\n\n'
                      'Entrer "HELP" pour avoir la description des commandes.\n'
                      'Entrer "EXIT" pour quitter l\'application.'),
        'HELP': ('Liste des actions possibles :\n '
                 'ADD | UPDATE | VIEW | DELETE\n\n '
                 'Liste des catégories possibles :\n '
                 'USER | CLIENT | CONTRACT | EVENT\n\n '
                 'Syntaxe : ACTION CATEGORIE\n\n'
                 'L\'accès à certaines actions est restreint en fonction des permissions.'
                 ' attribuées à votre département.\n\n'
                 'Pour les connaître taper PERMISSION'),
        'CONNECTION_FIRST_TIME': 'Bienvenue pour votre première connexion.\n\nVeuillez définir votre mot de passe.',
        'CONNECTION_SECOND_TIME': ('Bienvenue pour votre première connexion.\n\n'
                                   'Veuillez entrer une deuxième fois votre mot de passe.'),
        'ADD_USER_STOPPED': 'Création de l\'utilisateur annulé.'
}

BAD = {
        'EMAIL': 'Votre saisie ne correspond pas à une adresse mail.',
        'EMPLOYEE_NUMBER': 'Votre saisie ne correspond pas à un numéro d\'employé.',
        'DEPARTMENT': 'Votre saisie ne correspond pas à un département.',
        'SELECT_USER': 'Merci d\'entrer un nombre.',
        'SELECT_CLIENT': 'Merci d\'entrer un nombre.',
        'TOTAL_AMOUNT': 'Merci d\'entrer un nombre.',
        'REST_AMOUNT': 'Merci d\'entrer un nombre.',
        'SELECT_CONTRACT': 'Merci d\'entrer un nombre.',
        'PHONE': 'Numéro de téléphone incorrect.',
        'CONTRACT_STATUS': 'Cette réponse n\'est pas possible.\n\nMerci d\'indiquer y or n comme demandé.',
        'TOKEN': 'Vous avez été déconnecté, merci de vous reconnecter.',
}

FAILED = {
        'SELECT_USER': 'Ce numéro ne correspond pas à un utilisateur.',
        'SELECT_CLIENT': 'Ce numéro ne correspond pas à un client.',
        'SELECT_CONTRACT': 'Ce numéro ne correspond pas à un contrat.',
        'LOGIN': 'Vos identifiants sont inconnus\nL\'application va s\'arrêter.',
        'PASSWORD_MATCH': 'Les mots de passe ne sont pas identiques.',
        'PASSWORD_EMPTY': 'Votre mot de passe ne peut pas être vide.',
}
