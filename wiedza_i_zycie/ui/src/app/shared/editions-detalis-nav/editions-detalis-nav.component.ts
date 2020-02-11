import { Component, HostBinding, Input } from '@angular/core';

import { WizDataService } from 'src/app/editions/wiz-data.service';
import { NavCommunicationService } from '../nav-communication.service'

@Component({
  selector: 'app-editions-detalis-nav',
  templateUrl: './editions-detalis-nav.component.html',
  styleUrls: ['./editions-detalis-nav.component.scss']
})

export class EditionsDetalisNavComponent {

  showFiller = false;
  articles

  constructor(
    private navCommunicationService: NavCommunicationService,
    private wizDataService: WizDataService,
  ) { }

  ngOnInit() {

    this.navCommunicationService.change.subscribe(isOpen => {
      this.isOpen = isOpen;
    });

    this.wizDataService.getWizJson().subscribe(data => {
      console.log(data[0]);
      this.articles = data['articles'];
    });
  }

  @HostBinding('class.is-open') @Input()
  isOpen = false;

  closeNav() {
    // this.navCommunicationService.changeLeftNavState();
    this.isOpen = !this.isOpen;
  }

}
