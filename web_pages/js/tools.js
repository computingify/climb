export function addLogoToPage() {
    const banner = document.createElement('div');
    const logo = document.createElement('img');
    logo.src = '/resources/logo.png'; // Path to the logo image
    logo.alt = 'Logo'; // Alternative text for the image

    // Add CSS classes for styling
    banner.classList.add('logo-banner');
    logo.classList.add('banner-logo');

    // Append the logo to the banner
    banner.appendChild(logo);

    // Insert the banner at the top of the body
    document.body.insertBefore(banner, document.body.firstChild);
}