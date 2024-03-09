// Überprüfen, ob die URL den Query-Parameter 'email_exists' enthält
$(document).ready(function() {
    // Überprüfen, ob die URL den Query-Parameter 'email_exists' enthält
    const urlParams = new URLSearchParams(window.location.search);
    const emailExists = urlParams.get('email_exists');
    const usernameExists = urlParams.get('username_exists');
    const passwordMatch = urlParams.get('password_match');

    // Wenn 'email_exists' gesetzt ist, zeigen Sie die Warnung an
    if (emailExists) {
        $('#emailWarning').removeClass('d-none');
        $('#registerModal').modal('show');

        // Entfernen Sie den Parameter aus der URL
        history.replaceState(null, null, window.location.pathname);
    }

    if (usernameExists) {
        $('#usernameWarning').removeClass('d-none');
        $('#registerModal').modal('show');

        // Entfernen Sie den Parameter aus der URL
        history.replaceState(null, null, window.location.pathname);
    }

    if (passwordMatch) {
        $('#passwordWarning').removeClass('d-none');
        $('#registerModal').modal('show');

        // Entfernen Sie den Parameter aus der URL
        history.replaceState(null, null, window.location.pathname);
    }

});


$(document).ready(function() {
    // Überprüfen, ob Flash-Nachrichten vorhanden sind
    if ($('#flashModal .alert').length > 0) {
        $('#flashModal').modal('show');
    }
});
