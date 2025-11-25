// JavaScript для пользовательских страниц

document.addEventListener('DOMContentLoaded', function() {
    initAuthForms();
    initProfileInteractions();
});

// Инициализация форм авторизации
function initAuthForms() {
    const loginForm = document.querySelector('form[method="POST"]');

    if (loginForm) {
        loginForm.addEventListener('submit', function(e) {
            const username = this.querySelector('#id_username');
            const password = this.querySelector('#id_password, #id_password1');

            if (username && password) {
                if (!username.value.trim()) {
                    e.preventDefault();
                    showFieldError(username, 'Введите имя пользователя');
                    return;
                }

                if (!password.value.trim()) {
                    e.preventDefault();
                    showFieldError(password, 'Введите пароль');
                    return;
                }
            }
        });
    }
}

// Взаимодействия в профиле
function initProfileInteractions() {
    // Подсветка строк в таблице
    const tableRows = document.querySelectorAll('.table-hover tbody tr');

    tableRows.forEach(row => {
        row.addEventListener('click', function() {
            this.classList.toggle('table-active');
        });
    });

    // Анимация карточек статистики
    const statsCards = document.querySelectorAll('.stats-card');

    statsCards.forEach(card => {
        card.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-5px) scale(1.02)';
        });

        card.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0) scale(1)';
        });
    });
}

// Вспомогательные функции
function showFieldError(field, message) {
    // Убираем старые ошибки
    const existingError = field.parentNode.querySelector('.field-error');
    if (existingError) {
        existingError.remove();
    }

    // Добавляем новую ошибку
    const errorDiv = document.createElement('div');
    errorDiv.className = 'field-error text-danger small mt-1';
    errorDiv.textContent = message;
    field.parentNode.appendChild(errorDiv);

    // Подсвечиваем поле
    field.classList.add('is-invalid');

    // Фокусируемся на поле
    field.focus();
}

// Валидация пароля при регистрации
function validatePassword(password) {
    const minLength = 8;
    const hasUpperCase = /[A-Z]/.test(password);
    const hasLowerCase = /[a-z]/.test(password);
    const hasNumbers = /\d/.test(password);
    const hasSpecialChar = /[!@#$%^&*(),.?":{}|<>]/.test(password);

    return {
        isValid: password.length >= minLength && hasUpperCase && hasLowerCase && hasNumbers,
        issues: [
            password.length < minLength ? `Пароль должен содержать минимум ${minLength} символов` : null,
            !hasUpperCase ? 'Пароль должен содержать заглавные буквы' : null,
            !hasLowerCase ? 'Пароль должен содержать строчные буквы' : null,
            !hasNumbers ? 'Пароль должен содержать цифры' : null
        ].filter(issue => issue !== null)
    };
}