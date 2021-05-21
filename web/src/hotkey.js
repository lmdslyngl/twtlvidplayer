
import Store from "./store.js";

export class Hotkey {
  static init() {
    document.addEventListener("keydown", (evt) => {
      Hotkey.onKeyDown(evt);
    });
  }

  static onKeyDown(evt) {
    if( evt.key === "j" ) {
      Store.nextVideo();
    } else if( evt.key == "k" ) {
      Store.prevVideo();
    }
  }

}
