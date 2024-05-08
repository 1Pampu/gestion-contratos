// CREATE TOAST
function createToast(body, title = 'Notificación') {
    const toast = document.createElement('div')
    toast.classList.add('toast', 'fade', 'show')
    toast.setAttribute('role', 'alert')
    toast.setAttribute('aria-live', 'assertive')
    toast.setAttribute('aria-atomic', 'true')
    toast.innerHTML = `
                <div class="toast-header">
                    <strong class="me-auto">${title}</strong>
                    <small>Ahora</small>
                    <button type="button" class="btn-close" data-bs-dismiss="toast" aria-label="Close"></button>
                </div>
                <div class="toast-body">
                    ${body}
                </div>
                `
    document.querySelector('.toast-container').appendChild(toast)
}