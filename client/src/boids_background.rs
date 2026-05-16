use yew::{html, Component, Context, Html};

use crate::settings::Settings;
use crate::simulation::Simulation;

pub struct BoidsBackground;

impl Component for BoidsBackground {
    type Message = ();
    type Properties = ();

    fn create(_ctx: &Context<Self>) -> Self {
        Self
    }

    fn view(&self, _ctx: &Context<Self>) -> Html {
        // Tuned-down flock for ambient background; readability matters more than density.
        let settings = Settings {
            boids: 160,
            ..Settings::default()
        };

        html! {
            <div class="boids-background" aria-hidden="true">
                <Simulation settings={settings} />
            </div>
        }
    }
}
