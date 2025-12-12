import { Component, Output, EventEmitter } from '@angular/core';

@Component({
  selector: 'app-topbar',
  standalone: true,
  templateUrl: './topbar.component.html',
  styleUrls: ['./topbar.component.css']
})
export class TopbarComponent {

  @Output() methodSelected = new EventEmitter<string>();

  chooseMethod(method: string) {
    this.methodSelected.emit(method);
  }
}
