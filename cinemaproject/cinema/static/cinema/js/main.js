// Основной JavaScript файл для кинокассы

document.addEventListener('DOMContentLoaded', function() {
    // Инициализация всех компонентов
    initBookingSystem();
    initMovieFilters();
    initSessionSelector();
});

// Система бронирования
function initBookingSystem() {
    const seatInput = document.getElementById('seats');
    const priceDisplay = document.getElementById('total-price');
    const pricePerSeat = parseFloat(document.getElementById('price-per-seat').value);

    if (seatInput && priceDisplay) {
        seatInput.addEventListener('input', function() {
            const seats = parseInt(this.value) || 0;
            const total = seats * pricePerSeat;
            priceDisplay.textContent = total.toFixed(2);
        });
    }
}

// Фильтры для фильмов
function initMovieFilters() {
    const filterButtons = document.querySelectorAll('.filter-btn');

    filterButtons.forEach(btn => {
        btn.addEventListener('click', function() {
            const genre = this.getAttribute('data-genre');
            filterMovies(genre);

            // Обновляем активную кнопку
            filterButtons.forEach(b => b.classList.remove('active'));
            this.classList.add('active');
        });
    });
}

function filterMovies(genre) {
    const movies = document.querySelectorAll('.movie-card');

    movies.forEach(movie => {
        if (genre === 'all' || movie.getAttribute('data-genre') === genre) {
            movie.style.display = 'block';
            setTimeout(() => {
                movie.classList.add('fade-in');
            }, 50);
        } else {
            movie.classList.remove('fade-in');
            movie.style.display = 'none';
        }
    });
}

// Выбор сеанса
function initSessionSelector() {
    const sessionButtons = document.querySelectorAll('.session-time:not(.disabled)');

    sessionButtons.forEach(btn => {
        btn.addEventListener('click', function(e) {
            e.preventDefault();

            // Убираем активный класс у всех кнопок
            sessionButtons.forEach(b => b.classList.remove('active'));

            // Добавляем активный класс текущей кнопке
            this.classList.add('active');

            // Показываем форму бронирования
            const bookingForm = document.getElementById('booking-form');
            if (bookingForm) {
                bookingForm.scrollIntoView({ behavior: 'smooth' });
            }
        });
    });
}

// Валидация форм
function validateBookingForm(form) {
    const seats = form.querySelector('#seats').value;
    const name = form.querySelector('#name').value;

    if (seats < 1) {
        alert('Пожалуйста, выберите хотя бы одно место');
        return false;
    }

    if (!name.trim()) {
        alert('Пожалуйста, введите ваше имя');
        return false;
    }

    return true;
}

// Утилиты
function formatTime(dateString) {
    const date = new Date(dateString);
    return date.toLocaleTimeString('ru-RU', {
        hour: '2-digit',
        minute: '2-digit'
    });
}

function formatDate(dateString) {
    const date = new Date(dateString);
    return date.toLocaleDateString('ru-RU', {
        weekday: 'long',
        year: 'numeric',
        month: 'long',
        day: 'numeric'
    });
}

// Дополнительные функции для основного приложения

// Инициализация всех компонентов при загрузке страницы
document.addEventListener('DOMContentLoaded', function() {
    initTooltips();
    initAlerts();
    initLazyLoading();
    initSmoothScrolling();
});

// Инициализация tooltips
function initTooltips() {
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function(tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
}

// Автоматическое скрытие alert'ов
function initAlerts() {
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(alert => {
        setTimeout(() => {
            const bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        }, 5000);
    });
}

// Ленивая загрузка изображений
function initLazyLoading() {
    const lazyImages = [].slice.call(document.querySelectorAll('img.lazy'));

    if ('IntersectionObserver' in window) {
        const lazyImageObserver = new IntersectionObserver(function(entries, observer) {
            entries.forEach(function(entry) {
                if (entry.isIntersecting) {
                    const lazyImage = entry.target;
                    lazyImage.src = lazyImage.dataset.src;
                    lazyImage.classList.remove('lazy');
                    lazyImageObserver.unobserve(lazyImage);
                }
            });
        });

        lazyImages.forEach(function(lazyImage) {
            lazyImageObserver.observe(lazyImage);
        });
    }
}

// Плавная прокрутка
function initSmoothScrolling() {
    const scrollLinks = document.querySelectorAll('a[href^="#"]');

    scrollLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();

            const targetId = this.getAttribute('href');
            if (targetId === '#') return;

            const targetElement = document.querySelector(targetId);
            if (targetElement) {
                targetElement.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });
}

// Форматирование дат
function formatDateTime(dateString) {
    const date = new Date(dateString);
    const now = new Date();
    const diffTime = Math.abs(now - date);
    const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));

    if (diffDays === 1) {
        return 'Сегодня в ' + date.toLocaleTimeString('ru-RU', { hour: '2-digit', minute: '2-digit' });
    } else if (diffDays === 2) {
        return 'Вчера в ' + date.toLocaleTimeString('ru-RU', { hour: '2-digit', minute: '2-digit' });
    } else if (diffDays <= 7) {
        return date.toLocaleDateString('ru-RU', { weekday: 'long', hour: '2-digit', minute: '2-digit' });
    } else {
        return date.toLocaleDateString('ru-RU', {
            year: 'numeric',
            month: 'long',
            day: 'numeric',
            hour: '2-digit',
            minute: '2-digit'
        });
    }
}

// Управление состоянием загрузки
function setLoadingState(element, isLoading) {
    if (isLoading) {
        element.classList.add('loading');
        element.disabled = true;
        element.innerHTML = '<span class="spinner-border spinner-border-sm" role="status"></span> Загрузка...';
    } else {
        element.classList.remove('loading');
        element.disabled = false;
        // Восстанавливаем оригинальный текст
        // Нужно хранить оригинальный текст в data-атрибуте
        const originalText = element.dataset.originalText;
        if (originalText) {
            element.innerHTML = originalText;
        }
    }
}

// Валидация форм
function validateForm(form) {
    let isValid = true;
    const requiredFields = form.querySelectorAll('[required]');

    requiredFields.forEach(field => {
        if (!field.value.trim()) {
            isValid = false;
            field.classList.add('is-invalid');

            // Создаем сообщение об ошибке
            let errorMessage = field.parentNode.querySelector('.field-error');
            if (!errorMessage) {
                errorMessage = document.createElement('div');
                errorMessage.className = 'field-error text-danger small mt-1';
                errorMessage.textContent = 'Это поле обязательно для заполнения';
                field.parentNode.appendChild(errorMessage);
            }
        } else {
            field.classList.remove('is-invalid');
            const errorMessage = field.parentNode.querySelector('.field-error');
            if (errorMessage) {
                errorMessage.remove();
            }
        }
    });

    return isValid;
}

// Утилита для работы с локальным хранилищем
const storage = {
    set: (key, value) => {
        try {
            localStorage.setItem(key, JSON.stringify(value));
            return true;
        } catch (e) {
            console.error('Ошибка сохранения в localStorage:', e);
            return false;
        }
    },

    get: (key, defaultValue = null) => {
        try {
            const item = localStorage.getItem(key);
            return item ? JSON.parse(item) : defaultValue;
        } catch (e) {
            console.error('Ошибка чтения из localStorage:', e);
            return defaultValue;
        }
    },

    remove: (key) => {
        try {
            localStorage.removeItem(key);
            return true;
        } catch (e) {
            console.error('Ошибка удаления из localStorage:', e);
            return false;
        }
    }
};

// Экспорт функций для глобального использования
window.CinemaApp = {
    formatDateTime,
    setLoadingState,
    validateForm,
    storage,
    initTooltips,
    initAlerts
};
