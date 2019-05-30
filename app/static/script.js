// Make Log in button display log in form

// use JS to get button element and hidden_elem, and onclick change hidden_elem to default display.
// THINK WE HAVE BUTTONS WHERE WE SHOULD HAVE <INPUT TYPE=SUBMIT>

// document.getElementById("display-login").setAttribute("display", "none");

document.getElementById("display-login")
  .addEventListener("click", displayLogin);

function displayLogin() {
  document.getElementById("display-login").style.display = "none";
  document.querySelectorAll(".hidden_elem")[0].style.display = "block";
  // el = document.querySelectorAll(".hidden_elem");
  // console.log(el[0]);
  // change display attribute to..
  // el.classList.remove("")
}

// If you’re hiding text on a FAQ page with the intention of showing it with JS, you should also hide it with JS, otherwise, people using regular CSS enabled browsers but with JS disabled JS will never be able to see the text, leaving you with an unusable FAQ’s page!

// When hiding something with the intention of showing it with JS, you should also hide it with JS, otherwise, people using regular CSS enabled browsers, but with JS disabled, JS will never be able to see the text.
// Excellent point. Remove it (visually) once the DOM loads.

// front end dev should use a screen reader for a little bit: NVDA, Orca, VoiceOver

// Learn all you can about accessibility, then ask this if still not sure, in reactiflux general:
// Regarding the "log in to Existing Account" on facebook sign up page that when clicked is replaced by the login form. They use jquery css.hide() and css.show(). How does this affect screen readers?

// ----------------------
// I always thought positioning elements off the screen to hide them was a hacky method, and display: none was what you where supposed to do but I've just read in a 2012 css-tricks article that display: none is bad for screen readers. I'm duplicating the facebook login on the signup page.It has a button that when clicked disappears and the login form appears in it's place. Fyi, they have used display: none; on the form and use jquery css.hide() and css.show()

// none is good for screen readers when used correctly
// It says don't consider this element
// the issue in that setup would be the javascript to hide / show it

// so the screen reader would read the button, and then it could read the form once it becomes display: block ? (after clicking)

// The issue in the setup is the javascript to do that

// what do you mean ?

// The functionality you're describing should not happen for screen readers, there should be no showing/hiding things
// Because that's not the consideration of a screen reader
// If you're aiming for accessibility, you should provide a version of your site that works for screen readers and other clients where the common Javascript approaches fail
// webaim is the best place for reading about accessibility - Archelause
// --------------------

// /^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/





