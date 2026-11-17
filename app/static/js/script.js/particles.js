
/* ==========================================
   CINEFOLIO - VISIBLE FLOATING PARTICLES
========================================== */

document.addEventListener("DOMContentLoaded", () => {

    const pages = document.querySelectorAll(
        ".login-page, .register-page"
    );

    if (!pages.length) return;

    const reducedMotion = window.matchMedia(
        "(prefers-reduced-motion: reduce)"
    ).matches;

    pages.forEach((page) => {

        // Avoid creating duplicate canvases
        if (page.querySelector(".particle-canvas")) return;

        const canvas = document.createElement("canvas");
        canvas.className = "particle-canvas";

        page.prepend(canvas);

        const ctx = canvas.getContext("2d");

        if (!ctx) return;

        let width = 0;
        let height = 0;
        let particles = [];
        let animationFrame;

        const particleCount =
            window.innerWidth < 768 ? 35 : 100;

        const mouse = {
            x: null,
            y: null,
            radius: 120
        };

        // Set canvas dimensions
        function resizeCanvas() {

            const rect = page.getBoundingClientRect();

            width = rect.width;
            height = rect.height;

            const ratio = Math.min(
                window.devicePixelRatio || 1,
                2
            );

            canvas.width = width * ratio;
            canvas.height = height * ratio;

            ctx.setTransform(
                ratio, 0, 0, ratio, 0, 0
            );

            createParticles();
        }

        // Create glowing particles
        function createParticles() {

            particles = [];

            for (let i = 0; i < particleCount; i++) {

                particles.push({

                    x: Math.random() * width,
                    y: Math.random() * height,

                    size: Math.random() * 2 + 0.8,

                    speedX: (Math.random() - 0.5) * 0.45,
                    speedY: -(Math.random() * 0.65 + 0.12),

                    opacity: Math.random() * 0.5 + 0.35,

                    pulse: Math.random() * Math.PI * 2,

                    glow: Math.random() * 12 + 7

                });
            }
        }

        // Render particles
        function drawParticles() {

            ctx.clearRect(0, 0, width, height);

            particles.forEach((particle) => {

                particle.x += particle.speedX;
                particle.y += particle.speedY;

                particle.pulse += 0.025;

                // Reset when leaving the screen
                if (particle.y < -15) {
                    particle.y = height + 15;
                    particle.x = Math.random() * width;
                }

                if (particle.x < -15) {
                    particle.x = width + 15;
                }

                if (particle.x > width + 15) {
                    particle.x = -15;
                }

                // Gentle mouse interaction
                if (mouse.x !== null && mouse.y !== null) {

                    const dx = particle.x - mouse.x;
                    const dy = particle.y - mouse.y;

                    const distance = Math.sqrt(
                        dx * dx + dy * dy
                    );

                    if (distance < mouse.radius && distance > 0) {

                        const force =
                            (mouse.radius - distance) / mouse.radius;

                        particle.x += dx / distance * force * 1.2;
                        particle.y += dy / distance * force * 1.2;
                    }
                }

                const opacity =
                    particle.opacity *
                    (0.75 + Math.sin(particle.pulse) * 0.25);

                // Draw glow
                ctx.beginPath();

                ctx.arc(
                    particle.x,
                    particle.y,
                    particle.size,
                    0,
                    Math.PI * 2
                );

                ctx.fillStyle =
                    `rgba(255, 65, 95, ${opacity})`;

                ctx.shadowBlur = particle.glow;

                ctx.shadowColor =
                    "rgba(230, 35, 75, 0.95)";

                ctx.fill();

            });

            ctx.shadowBlur = 0;
        }

        // Animation loop
        function animate() {

            drawParticles();

            if (!reducedMotion) {
                animationFrame =
                    requestAnimationFrame(animate);
            }
        }

        // Mouse movement
        page.addEventListener("mousemove", (event) => {

            const rect = page.getBoundingClientRect();

            mouse.x = event.clientX - rect.left;
            mouse.y = event.clientY - rect.top;

        });

        page.addEventListener("mouseleave", () => {

            mouse.x = null;
            mouse.y = null;

        });

        // Initialize
        resizeCanvas();
        animate();

        // Update on resize
        const observer = new ResizeObserver(() => {

            resizeCanvas();

            if (reducedMotion) {
                drawParticles();
            }

        });

        observer.observe(page);

        // Clean up if page is removed
        window.addEventListener("pagehide", () => {
            cancelAnimationFrame(animationFrame);
            observer.disconnect();
        }, { once: true });

    });

});
