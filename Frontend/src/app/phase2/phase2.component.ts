import { Component } from '@angular/core';
import { TopbarComponent } from '../components/topbar/topbar.component';
import { InputComponent } from '../components/input/input.component';

@Component({
  selector: 'app-phase2',
  standalone: true,
  imports: [TopbarComponent, InputComponent],
  templateUrl: './phase2.component.html',
  styleUrls: ['./phase2.component.css'],
})
export class Phase2Component {
  selectedMethod: string = '';

  selectMethod(method: string) {
    this.selectedMethod = method;
  }
}
