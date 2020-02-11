import { Component, ViewChild } from '@angular/core';
import { MatSidenav } from '@angular/material/sidenav';

@Component({
  selector: 'app-editions',
  templateUrl: './editions.component.html',
  styleUrls: ['./editions.component.scss']
})
export class EditionsComponent {

  @ViewChild('editions', { static: true }) editions: MatSidenav;

  selectedEditionDate: string;

  onEditionSelected(selectedEditionDate) {
    this.selectedEditionDate = selectedEditionDate;
    this.editions.open();
  }
}
