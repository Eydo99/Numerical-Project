import { Component } from '@angular/core';
import { TopbarComponent } from '../components/topbar/topbar.component';
import { InputComponent } from '../components/input/input.component';
import { OutputComponent } from '../components/output/output.component';

@Component({
  selector: 'app-phase2',
  standalone: true,
  imports: [TopbarComponent, InputComponent, OutputComponent],
  templateUrl: './phase2.component.html',
  styleUrls: ['./phase2.component.css'],
})
export class Phase2Component {
  selectedMethod: string = '';
  solution: number | null = null;
  iterations: number = 0;
  executionTime: number = 0;
  steps: any[] = [];
  error: string | null = null;
  convergenceStatus: number | null = null;
  plotImageUrl: string | null = null;
  selectMethod(method: string) {
    this.selectedMethod = method;
    this.clearResults();
  }
  handleSolveComplete(result: any) {
    this.solution = result.solution;
    this.iterations = result.iterations;
    this.executionTime = result.executionTime;
    this.steps = result.steps;
    this.error = result.error;
    this.convergenceStatus = result.convergenceStatus;
  }
  handlePlotComplete(imageUrl: string) {
    this.plotImageUrl = imageUrl;
  }

  clearResults() {
    this.solution = null;
    this.iterations = 0;
    this.executionTime = 0;
    this.steps = [];
    this.error = null;
    this.convergenceStatus = null;
  }

}
