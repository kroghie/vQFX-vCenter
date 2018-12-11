#!/usr/bin/env python

"""
Python program for listing the vms on an ESX / vCenter host
"""

from __future__ import print_function

from pyVim.connect import SmartConnect, Disconnect, SmartConnectNoSSL
from pyVmomi import vim

import argparse
import atexit
import getpass
import ssl

def GetArgs():
   """
   Supports the command-line arguments listed below.
   """
   parser = argparse.ArgumentParser(
       description='Process args for connecting to vCenter or esxi host')
   parser.add_argument('-s', '--host', required=True, action='store',
                       help='Remote host to connect to')
   parser.add_argument('-o', '--port', type=int, default=443, action='store',
                       help='Port to connect on')
   parser.add_argument('-u', '--user', required=True, action='store',
                       help='User name to use when connecting to host')
   parser.add_argument('-p', '--password', required=False, action='store',
                       help='Password to use when connecting to host')
   parser.add_argument('-insecure','--insecure', required=False, action='store_true',
                       help='Disable SSL check for self-signed certificates')
   parser.add_argument('-vmname','--vmname', required=True, action='store', dest="vmname",
                       help='VM to add vmdk')
   parser.add_argument('-vmdkpath','--vmdkpath', required=True, action='store',dest="vmdkpath",
                       help='Path to VMDK file')



   args = parser.parse_args()
   return args

def add_disk(vm, service_instance):
  args = GetArgs()

  a = 0
  spec = vim.vm.ConfigSpec()
  unit_number = 0
  for dev in vm.config.hardware.device:
    if hasattr(dev.backing, 'fileName') or isinstance(dev, vim.vm.device.VirtualCdrom):
          unit_number = int(dev.unitNumber) + 1
    # elif vim.vm.device.VirtualCdrom:
    #       unit_number = int(dev.unitNumber) + 1

    if isinstance(dev, vim.vm.device.VirtualIDEController):
        while a == 0:
            controller = dev
            a+=1

  # add disk here
  dev_changes = []
  disk_spec = vim.vm.device.VirtualDeviceSpec()
  disk_spec.operation = vim.vm.device.VirtualDeviceSpec.Operation.add
  disk_spec.device = vim.vm.device.VirtualDisk()
  disk_spec.device.backing = vim.vm.device.VirtualDisk.FlatVer2BackingInfo(fileName=args.vmdkpath)
  disk_spec.device.backing.thinProvisioned = True
  disk_spec.device.backing.diskMode = 'persistent'
  disk_spec.device.unitNumber = unit_number
  #  disk_spec.device.capacityInKB = new_disk_kb
  disk_spec.device.controllerKey = controller.key
  dev_changes.append(disk_spec)
  print(disk_spec)
  spec.deviceChange = dev_changes
  vm.ReconfigVM_Task(spec=spec)
  print (controller)

def get_obj(content, vimtype, name):
    """
    Get the vsphere object associated with a given text name
    """
    obj = None
    container = content.viewManager.CreateContainerView(content.rootFolder, vimtype, True)
    for c in container.view:
        if c.name == name:
            obj = c
            break
    return obj

def main():

#Check SSL options and connect to vCenter
    args = GetArgs()


    if(args.insecure):
        service_instance = SmartConnectNoSSL(host=args.host, user=args.user, pwd=args.password, port=int(args.port))
    else:
        service_instance = SmartConnect(host=args.host, user=args.user, pwd=args.password, port=int(args.port))

#Add disk
    vm = get_obj(service_instance.RetrieveContent(), [vim.VirtualMachine], args.vmname)
    add_disk(vm, service_instance)

# Start program
if __name__ == '__main__':
     main()
