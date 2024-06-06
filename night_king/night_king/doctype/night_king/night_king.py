# Copyright (c) 2024, The Commit Company and contributors
# For license information, please see license.txt
import faker

import frappe
from frappe.model.document import Document


class NightKing(Document):

	@frappe.whitelist()
	def create_raven_users(self):
		# Create multiple raven users

		# Get the number of users to create
		number_of_users = self.number_of_users

		number_created = 0
		# Create the users
		for i in range(number_of_users):

			try:

				first_name = faker.Faker().first_name()
				last_name = faker.Faker().last_name()
				user = frappe.new_doc("User")
				user.email = "{}.{}@raven.com".format(first_name, last_name).lower()
				user.send_welcome_email = 0
				user.first_name = first_name
				user.last_name = last_name

				# Add a profile image
				user.user_image = "https://i.pravatar.cc/300?u={}".format(user.email)

				# Add the role
				user.append_roles("Raven User")

				# Save the user
				user.insert()

				# Commit since there might be duplicates
				frappe.db.commit()

				number_created += 1

			except:
				continue
			frappe.publish_progress(percent=(i + 1/number_of_users)*100, title="Creating Users", description="Creating user {}".format(i))

		frappe.msgprint("{} Users created successfully".format(number_created), title="Success", indicator="green", alert=True)


	@frappe.whitelist()
	def generate_reactions(self):
		'''
		 Generate reactions for the users in the latest message in the general channel
		'''
		last_general_channel_message = frappe.get_all("Raven Message", filters={"channel_id": "general"}, pluck='name', order_by="creation desc", limit=1)

		if not last_general_channel_message:
			frappe.msgprint("No messages in the general channel", title="Error", indicator="red", alert=True)
			return
		
		last_general_channel_message = last_general_channel_message[0]

		# Get 100 random Raven Users
		raven_users = frappe.get_all("Raven User", filters={"name": ["like", "%raven%"]}, pluck='user', limit=100)

		# Generate a reaction for each user
		for user in raven_users:
			reaction = frappe.new_doc("Raven Message Reaction")
			reaction.reaction = "🎉"
			reaction.message = last_general_channel_message
			reaction.owner = user
			reaction.insert()
			# Explicitly set the user to the user who reacted in owner and modified_by
			frappe.db.sql("UPDATE `tabRaven Message Reaction` SET owner = '{}', modified_by = '{}' WHERE name = '{}'".format(user, user, reaction.name))

	pass
