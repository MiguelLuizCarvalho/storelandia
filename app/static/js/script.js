async function loadProducts() {
    const url = "http://127.0.0.1:5000/api/products/";
    const resposta = await fetch(url);
    const dados = await resposta.json();

    const products = document.getElementById('productsCards');

    products.innerHTML = dados.map(produto => `
        <div class="col-md-4 mb-4">
            <div class="card shadow-sm">
                <div class="card-body">
                    <h5 class="card-title">${produto.name}</h5>
                    <p class="card-text text-muted">${produto.description}</p>
                    <p class="h5 text-primary">R$ ${produto.price}</p>
                    <button class="btn btn-success w-100">Comprar</button>
                </div>
            </div>
        </div>
    `).join('');
}

loadProducts();