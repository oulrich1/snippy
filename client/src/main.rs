mod boid;
mod boids_background;
mod math;
mod settings;
mod simulation;

use boids_background::BoidsBackground;
use yew::{html, Component, Context, Html};

struct Portfolio;

impl Component for Portfolio {
    type Message = ();
    type Properties = ();

    fn create(_ctx: &Context<Self>) -> Self {
        Self
    }

    fn view(&self, _ctx: &Context<Self>) -> Html {
        html! {
            <>
                <BoidsBackground />
                <a class="skip-link" href="#main">{"Skip to content"}</a>
                <header class="site-header">
                    <a class="brand" href="#top">{"Oriah Ulrich"}</a>
                    <nav class="site-nav" aria-label="Primary">
                        <a href="#about">{"About"}</a>
                        <a href="#focus">{"Focus"}</a>
                        <a href="#footprint">{"Public record"}</a>
                        <a href="#lab">{"Lab & blog"}</a>
                    </nav>
                </header>
                <main id="main">
                    <section id="top" class="hero">
                        <p class="eyebrow">{"Software · simulations · agentic systems"}</p>
                        <h1>{"Building and exploring emergent behavior"}</h1>
                        <p class="hero__lede">
                            {"I am a software engineer with a long arc across platform work, applied ML interests, and hands-on graphics and simulation. This site highlights who I am, what I have shipped in public, and where I am headed next—including experiments in "}
                            <strong>{"agentic systems"}</strong>
                            {" written up as I go."}
                        </p>
                        <p class="hero__aside">
                            {"The flock drifting behind this page is a Reynolds-style boids simulation running in Rust + WebAssembly—an ambient nod to the kind of emergent agent behavior I like to build."}
                        </p>
                        <div class="hero__actions">
                            <a class="button button--primary" href="https://github.com/oulrich1">{"GitHub"}</a>
                            <a class="button button--ghost" href="https://www.linkedin.com/in/oriaheu/">{"LinkedIn"}</a>
                            <a class="button button--ghost" href="https://devpost.com/oulrich">{"Devpost"}</a>
                        </div>
                    </section>

                    <section id="about" class="section section--tight">
                        <h2>{"About"}</h2>
                        <div class="prose">
                            <p>
                                {"I care about systems that stay understandable as they grow: clear boundaries, observable behavior, and tooling that helps teams move without breaking trust. Professionally, that has meant platform engineering and products where correctness and throughput both matter."}
                            </p>
                            <p>
                                {"Recently I have been returning to a thread I have always enjoyed—"}
                                <strong>{"simulation, interaction, and autonomy"}</strong>
                                {". Agentic patterns (goals, perception, action loops, coordination) show up everywhere from game AI to orchestration stacks. I want to connect those ideas to small, reproducible experiments you can read about on the "}
                                <a href="#lab">{"lab page"}</a>
                                {"."}
                            </p>
                        </div>
                    </section>

                    <section id="focus" class="section">
                        <h2>{"What I bring"}</h2>
                        <ul class="card-grid">
                            <li class="card">
                                <h3>{"Platform & product engineering"}</h3>
                                <p>
                                    {"Shipping and operating services where reliability, security, and developer experience intersect—so product teams can iterate quickly without surprises."}
                                </p>
                            </li>
                            <li class="card">
                                <h3>{"Rust, WASM, and performance-minded UI"}</h3>
                                <p>
                                    {"This whole site is a "}
                                    <strong>{"Yew + WebAssembly"}</strong>
                                    {" front end. The flock you see behind the page runs entirely in your browser from a small, inspectable codebase."}
                                </p>
                            </li>
                            <li class="card">
                                <h3>{"Simulations & agentic systems"}</h3>
                                <p>
                                    {"Emergent flocking is a classic sandbox for rules-based autonomy. I am extending that curiosity toward richer agent loops, tooling, and write-ups as I prototype."}
                                </p>
                            </li>
                        </ul>
                    </section>

                    <section id="footprint" class="section section--alt">
                        <h2>{"Public record (research snapshot)"}</h2>
                        <p class="section__note">
                            {"The bullets below were assembled in May 2026 from "}
                            <strong>{"public profiles and APIs"}</strong>
                            {" (GitHub, Devpost, LinkedIn-style bios surfaced in search, and general web search). They are meant as a good-faith snapshot, not a primary source—follow the links for authoritative detail."}
                        </p>
                        <ul class="timeline">
                            <li>
                                <strong>{"GitHub (@oulrich1)"}</strong>
                                {" — Long-time open source presence with public repositories spanning C++, JavaScript, Java, and more; active contributor to community projects as of 2026."}
                            </li>
                            <li>
                                <strong>{"Devpost"}</strong>
                                {" — Hackathon-style builds such as "}
                                <em>{"PeruseWithSpritz"}</em>
                                {" (RSVP-style reading) and "}
                                <em>{"Fallng"}</em>
                                {", showing product thinking under time pressure."}
                            </li>
                            <li>
                                <strong>{"Career themes (from public bios)"}</strong>
                                {" — Platform engineering at scale; earlier work touched edge computing and virtualization, OCR and imaging with OpenCV, and desktop engineering in C++ / C#."}
                            </li>
                            <li>
                                <strong>{"Education"}</strong>
                                {" — B.S. in Computer Science (minor in Mathematics) from California State University, Chico; continued graduate study in data engineering and machine learning (public listings reference Georgia Tech online programs—verify on LinkedIn)."}
                            </li>
                        </ul>
                    </section>

                    <section id="lab" class="section">
                        <h2>{"Lab & blog (coming online)"}</h2>
                        <div class="prose">
                            <p>
                                {"I am standing up a writing habit for "}
                                <strong>{"short, experiment-forward posts"}</strong>
                                {": what I tried, what broke, what surprised me, and what I would try next. Expect threads on flocking and steering, lightweight agent architectures, procedural motion, and tooling for iteration."}
                            </p>
                            <p>
                                {"If you want a place to watch for essays while this site grows, my public "}
                                <a href="https://substack.com/profile/30376376-oriah">{"Substack profile"}</a>
                                {" is linked for follow-friendly updates."}
                            </p>
                        </div>
                    </section>
                </main>
                <footer class="site-footer">
                    <p>
                        {"© Oriah Ulrich · "}
                        <a href="https://oriahulrich.com">{"oriahulrich.com"}</a>
                        {" · "}
                        <a href="public-footprint.html">{"Public footprint (sources)"}</a>
                        {" · Source: "}
                        <a href="https://github.com/oulrich1/snippy">{"snippy on GitHub"}</a>
                    </p>
                </footer>
            </>
        }
    }
}

fn main() {
    yew::Renderer::<Portfolio>::new().render();
}
