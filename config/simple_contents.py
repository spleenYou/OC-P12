NORMAL = {
        'FIRST_LAUNCH': 'Un utilisateur de l\'équipe Management va être créé\nafin de pouvoir continuer.',
        'NO_CLIENT_WITHOUT_EVENT': 'Pas de client avec contrat sans évènement.',
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
                 'Pour les connaître taper PERMISSION\n\n'
                 'RESET PASSWORD pour redéfinir votre mot de passe'),
        'PASSWORD': 'Bienvenue pour votre première connexion.\n\nVeuillez définir votre mot de passe.',
}

ERROR = {
        'ADD_USER_STOPPED': ('Il faut au moins un utilisateur pour utiliser l\'application\n'
                             'Fermeture de l\'application'),
        'UNKNOWN': 'Cette commande est inconnue.',
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
        'PASSWORD': 'Votre mot de passe ne peut pas être vide.',

}

FAILED = {
        'EMAIL': 'Votre saisie ne correspond pas à une adresse mail.',
        'SELECT_USER': 'Ce numéro ne correspond pas à un utilisateur.',
        'SELECT_CLIENT': 'Ce numéro ne correspond pas à un client.',
        'SELECT_CONTRACT': 'Ce numéro ne correspond pas à un contrat.',
        'CONNECTION': 'Vos identifiants sont inconnus\nL\'application va s\'arrêter.',
        'PASSWORD': 'Les mots de passe ne sont pas identiques.',
}
