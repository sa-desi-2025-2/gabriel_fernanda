document.addEventListener('DOMContentLoaded', function() {
	function showFormError(form, msg) {
		if (!form) return;
		// Remove existing generic error
		var existing = form.querySelector('.form-error');
		if (existing) existing.remove();

		var div = document.createElement('div');
		div.className = 'alert alert-danger form-error';
		div.setAttribute('role', 'alert');
		div.textContent = msg;
		// insert as first child in card (if present) or before form
		var card = form.closest('.card');
		if (card) card.insertBefore(div, card.firstChild);
		else form.insertBefore(div, form.firstChild);
	}

	function clearFormErrorOnInput(form) {
		if (!form) return;
		form.addEventListener('input', function() {
			var existing = form.querySelector('.form-error');
			if (existing) existing.remove();
		});
	}

	// Login form validation
	var loginForm = document.getElementById('login-form');
	if (loginForm) {
		clearFormErrorOnInput(loginForm);
		loginForm.addEventListener('submit', function(e) {
			var usuario = loginForm.querySelector('#usuario') ? loginForm.querySelector('#usuario').value.trim() : '';
			var senha = loginForm.querySelector('#senha') ? loginForm.querySelector('#senha').value.trim() : '';
			if (!usuario || !senha) {
				e.preventDefault();
				showFormError(loginForm, 'Preencha usuário e senha.');
				return false;
			}
			return true;
		});
	}

	// Cadastro form validation
	var cadastroForm = document.getElementById('cadastro-form');
	if (cadastroForm) {
		clearFormErrorOnInput(cadastroForm);
		cadastroForm.addEventListener('submit', function(e) {
			var usuario = cadastroForm.querySelector('#usuario') ? cadastroForm.querySelector('#usuario').value.trim() : '';
			var email = cadastroForm.querySelector('#email') ? cadastroForm.querySelector('#email').value.trim() : '';
			var senha = cadastroForm.querySelector('#senha') ? cadastroForm.querySelector('#senha').value : '';
			var confirmar = cadastroForm.querySelector('#confirmar') ? cadastroForm.querySelector('#confirmar').value : '';

			if (!usuario || !email || !senha) {
				e.preventDefault();
				showFormError(cadastroForm, 'Preencha todos os campos.');
				return false;
			}
			if (senha !== confirmar) {
				e.preventDefault();
				showFormError(cadastroForm, 'As senhas não coincidem.');
				return false;
			}
			return true;
		});
	}

});

// Expose helper for debugging
window.__showFormError = function(formSelector, msg) {
	var form = document.querySelector(formSelector);
	if (!form) return;
	var evt = new Event('submit', { bubbles: true, cancelable: true });
	// show message directly
	var div = document.createElement('div');
	div.className = 'alert alert-danger';
	div.textContent = msg;
	var card = form.closest('.card');
	if (card) card.insertBefore(div, card.firstChild);
	else form.insertBefore(div, form.firstChild);
};
