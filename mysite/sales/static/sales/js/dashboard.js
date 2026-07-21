"use strict";

const productDataElement =
    document.getElementById("product-data");

const productList =
    document.getElementById("product-list");

const replayButton =
    document.getElementById("replay-button");

const productData = productDataElement
    ? JSON.parse(productDataElement.textContent)
    : [];

function findMaximumSales(products) {
    let maximumSales = 0;

    for (const product of products) {
        if (product.weeklySales > maximumSales) {
            maximumSales = product.weeklySales;
        }
    }

    return maximumSales;
}

function createImageSquare(product) {
    const square = document.createElement("div");

    square.classList.add("product-square");
    square.style.backgroundColor =
        product.color || "#2563eb";

    if (!product.imageUrl) {
        square.classList.add("image-placeholder");
        square.textContent =
            product.name.charAt(0).toUpperCase();

        return square;
    }

    const image = document.createElement("img");

    image.src = product.imageUrl;
    image.alt = product.name;
    image.loading = "lazy";

    image.addEventListener("error", () => {
        image.remove();

        square.classList.add("image-placeholder");
        square.textContent =
            product.name.charAt(0).toUpperCase();
    });

    square.appendChild(image);

    return square;
}

function createProduct(product, index) {
    const row =
        document.createElement("li");

    row.classList.add("product-row");

    const details =
        document.createElement("div");

    details.classList.add(
        "product-details"
    );

    const name =
        document.createElement("h2");

    name.textContent = product.name;

    const priceLine =
        document.createElement("p");

    priceLine.classList.add("price-line");

    const originalPrice =
        document.createElement("span");

    originalPrice.classList.add(
        "original-price"
    );

    originalPrice.textContent =
        `$${product.originalPrice.toFixed(2)}`;

    const salePrice =
        document.createElement("span");

    salePrice.classList.add("sale-price");

    salePrice.textContent =
        `$${product.salePrice.toFixed(2)}`;

    priceLine.append(
        originalPrice,
        salePrice
    );

    const salesCount =
        document.createElement("p");

    salesCount.classList.add("sales-count");

    salesCount.textContent =
        `${product.weeklySales} weekly sales`;

    details.append(
        name,
        priceLine,
        salesCount
    );

    const track =
        document.createElement("div");

    track.classList.add("animation-track");

    const movingProduct =
        document.createElement("div");

    movingProduct.classList.add("moving-product");

    const imageSquare =
        createImageSquare(product);

    const salesBadge =
        document.createElement("span");

    salesBadge.classList.add("sales-badge");
    salesBadge.textContent =
        product.weeklySales;

    movingProduct.append(
        imageSquare,
        salesBadge
    );

    track.appendChild(movingProduct);

    row.append(details, track);

    row.movingProduct = movingProduct;
    row.animationTrack = track;
    row.productData = product;

    return row;
}

function displayProducts(products) {
    productList.innerHTML = "";

    products.forEach(
        (product, index) => {
            productList.appendChild(
                createProduct(
                    product,
                    index
                )
            );
        }
    );
}

function animateProducts() {
    const maximumSales =
        findMaximumSales(productData);

    const rows =
        productList.querySelectorAll(
            ".product-row"
        );

    for (const row of rows) {
        const product =
            row.productData;

        const movingProduct =
            row.movingProduct;

        const availableDistance =
            Math.max(
                0,
                row.animationTrack.clientWidth -
                movingProduct.offsetWidth -
                20
            );

        const ratio =
            maximumSales > 0
                ? product.weeklySales /
                maximumSales
                : 0;

        movingProduct.style.setProperty(
            "--distance",
            `${availableDistance * ratio}px`
        );

        movingProduct.classList.toggle(
            "top-seller",
            product.weeklySales ===
            maximumSales
        );

        movingProduct.classList.remove(
            "animate"
        );

        void movingProduct.offsetWidth;

        movingProduct.classList.add(
            "animate"
        );
    }
}

displayProducts(productData);
animateProducts();

if (replayButton) {
    replayButton.addEventListener(
        "click",
        animateProducts
    );
}

window.addEventListener(
    "resize",
    animateProducts
);