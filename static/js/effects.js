document.addEventListener('DOMContentLoaded', () => {
    const animateTargets = document.querySelectorAll(
        '.kpi-card, .chart-card, .chart-page-card, .weather-table, #weather-result'
    );

    animateTargets.forEach((el) => el.classList.add('animate-on-scroll'));

    const observer = new IntersectionObserver(
        (entries) => {
            entries.forEach((entry) => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('in-view');
                }
            });
        },
        { threshold: 0.12 }
    );

    animateTargets.forEach((el) => observer.observe(el));
});
