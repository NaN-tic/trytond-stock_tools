Stock Tools Module
##################

The stock tools module add new model to manage shipments and do some actions
according shipment state.

Next button call: "next_STATE" (STATE is shipment state code).

You could define in a custom module new methods that the method name do some actions
to process a shipment, for example:

- Send shipment to printer.
- Send shipment to carrier to delivery.
- Change state.
- ...

There are two menus to manage Stock Tools:

- All. Show all shipments managed without employee. Access "Stock Tools Administrator" group.
- Default. Show all shipments managed with current employee (user preferences). Access "Stock Tools" group.

Default Nexts
-------------

There are default nexts methods to process/continue shipment to next state:

- Draft -> Waitint
- Waiting -> Assigned (assign_try)
- Assigned -> Packed
- Packed -> Done
