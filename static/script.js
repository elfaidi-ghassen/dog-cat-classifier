const input = document.getElementById('imageInput')
const preview = document.getElementById('preview')
const btn = document.getElementById('classifyBtn')


input.addEventListener('change', function() {
    if (!this.files[0]) return
    preview.src = URL.createObjectURL(this.files[0])
    preview.style.display = 'block'
    document.querySelector('.yellow-border').style.display = 'block'  // show border
    btn.disabled = false
    document.getElementById('result').textContent = ""
})


async function predict() {
    const file = input.files[0]
    if (!file) return

    btn.disabled = true
    btn.textContent = 'Classifying...'

    const formData = new FormData()
    formData.append('image', file)

    try {
        const res = await fetch('/predict', { method: 'POST', body: formData })
        const data = await res.json()
        document.getElementById('result').textContent = `${data.label} — ${data.confidence}% confidence`
    } catch(e) {
        alert('Something went wrong!')
    }

    btn.textContent = 'Classify'
    btn.disabled = false
}