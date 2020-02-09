import { TestBed } from '@angular/core/testing';

import { NavCommunicationService } from './nav-communication.service';

describe('NavCommunicationService', () => {
  beforeEach(() => TestBed.configureTestingModule({}));

  it('should be created', () => {
    const service: NavCommunicationService = TestBed.get(NavCommunicationService);
    expect(service).toBeTruthy();
  });
});
