---
name: Donations & Payments
about: Issues related to Stripe payment processing and donations
title: '[PAYMENT] '
labels: payments, stripe, donations
assignees: ''

---

## Payment Component

<!-- Which part of the payment system is this related to? -->

- [ ] Stripe integration
- [ ] Donation flow (post-ride)
- [ ] Payment processing
- [ ] Fee transparency
- [ ] Refunds/Disputes
- [ ] Payment security
- [ ] Other (describe below)

## Issue Description

<!-- A clear and concise description of the issue -->

## Current Behavior

<!-- Describe how payments currently work (if applicable) -->

## Desired Behavior

<!-- Describe how you think it should work -->

## Donation Policy Context

<!-- Important context about our donation model -->

**Key Principle:** Catholic Ride Share uses a **donation-based model**. Rides are offered by volunteer drivers, and riders can optionally offer donations after rides. There is **no required payment** for rides.

- [ ] This issue respects the donation-based model
- [ ] This issue requires deviation from donation model (explain why)

## Stripe Fee Handling

<!-- How should Stripe fees be handled? -->

- [ ] Display Stripe fees transparently to riders
- [ ] Calculate net amount after fees
- [ ] Other approach (describe)

## User Type

<!-- Who is affected by this issue? -->

- [ ] Riders (making donations)
- [ ] Drivers (receiving donations)
- [ ] Admins (managing payments)
- [ ] All users

## Security Considerations

<!-- Security and compliance concerns -->

- [ ] PCI DSS compliance
- [ ] Sensitive data handling
- [ ] Payment card data
- [ ] No security concerns

## Financial Reporting

<!-- Does this affect financial reporting or transparency? -->

- [ ] Yes, affects reporting
- [ ] No reporting impact
- [ ] Needs audit trail

## Testing Requirements

<!-- What testing is needed? -->

- [ ] Test mode testing (Stripe)
- [ ] Live payment testing
- [ ] Refund testing
- [ ] Edge case testing
- [ ] None required

## Non-Profit Consideration

<!-- How does this align with non-profit status? -->

## Additional Context

<!-- Add any other context, screenshots, or Stripe documentation references -->

## Related Issues

Related to #

---

**Note:** Payment handling must be transparent, secure, and align with our mission to serve the Catholic community. Never store credit card data directly.
