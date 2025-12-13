import { Component, Output, EventEmitter } from '@angular/core';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-topbar',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './topbar.component.html',
  styleUrls: ['./topbar.component.css']
})
export class TopbarComponent {

  @Output() methodSelected = new EventEmitter<string>();
  activeMethod: string = '';
  chooseMethod(method: string) {
    this.activeMethod = method;
    this.methodSelected.emit(method);
  }
}
